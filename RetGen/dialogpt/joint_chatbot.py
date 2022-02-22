# This Python file was modified by Qian Ci based on chatbot.py

import requests
import json
from os.path import abspath, dirname, exists, join
import argparse
import logging
from tqdm import trange
import tqdm
import torch
import torch.nn.functional as F
import numpy as np
import socket
import os, sys
import re
import logging
from functools import partial
from demo_utils import download_model_folder
import argparse
import subprocess as sp
from pytorch_pretrained_bert import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from gpt2_training.train_utils import get_eval_list_same_length, load_model, boolean_string, fix_state_dict_namespace
from chatbot import cut_seq_to_eos, top_filtering, generate_next_token, generate_sequence

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

EOS_ID = 50256


def run_model():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name_or_path', type=str, default='',
                        help='pretrained model name or path to local checkpoint')
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--load_checkpoint", '-c', type=str, default='')
    parser.add_argument("--fp16", type=boolean_string, default=False)
    parser.add_argument("--max_seq_length", type=int, default=128)

    parser.add_argument("--generation_length", type=int, default=20)
    parser.add_argument("--max_history", type=int, default=2)

    parser.add_argument("--temperature", type=float, default=1)
    parser.add_argument("--top_k", type=int, default=0)
    parser.add_argument("--top_p", type=float, default=0.9)

    parser.add_argument('--use_gpu', action='store_true')
    parser.add_argument("--gpu", type=int, default=0)

    args = parser.parse_args()
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)

    device = torch.device("cuda" if torch.cuda.is_available() and args.use_gpu else "cpu")
    n_gpu = torch.cuda.device_count()
    args.device, args.n_gpu = device, n_gpu

    np.random.seed(args.seed)
    torch.random.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)

    #### load the GPT-2 model
    config = GPT2Config.from_json_file(os.path.join(args.model_name_or_path, 'config.json'))
    enc = GPT2Tokenizer.from_pretrained(args.model_name_or_path)
    model = load_model(GPT2LMHeadModel(config), args.load_checkpoint, args, verbose=True)
    model.to(device)
    model.eval()

    history = []
    chat_mode = False
    raw_text = ''

    while bot_message != "Hope you've learnt some things today. Bye!":
        raw_text = input("USR >>> ")
        if len(raw_text) == 0:
            continue
        elif raw_text == 'chat mode':
            chat_mode = True
            print('Switched to chat mode')
            continue
        elif raw_text == 'stop chat':
            chat_mode = False
            print('Switched to quiz mode')
            continue
        elif not raw_text:
            print('Prompt should not be empty!')
            continue

        if chat_mode:
            history.append(raw_text)
            context_tokens = sum([enc.encode(h) + [EOS_ID] for h in history], [])  # + [EOS_ID]
            context_tokens = torch.tensor(context_tokens, device=device, dtype=torch.long).unsqueeze(0)
            position_ids = torch.arange(0, context_tokens.size(-1), dtype=torch.long, device=context_tokens.device)

            out = generate_sequence(model, context_tokens, position_ids=position_ids,
                                    length=args.generation_length, temperature=args.temperature,
                                    top_k=args.top_k, top_p=args.top_p)

            out = out.tolist()
            text = enc.decode(cut_seq_to_eos(out[0])).encode('ascii', 'ignore').decode('ascii')
            print("SYS >>> ", text)
            history.append(text)
            history = history[-(2 * args.max_history + 1):]

        else:
            print("Sending message now...")
            # Pass message to rasa and print response
            r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": raw_text})
            for i in r.json():
                bot_message = i['text']
                print("SYS >>> ",bot_message)

if __name__ == '__main__':
    PYTHON_EXE = 'python'
    MODEL_FOLDER = './models'
    DATA_FOLDER = './data'

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    if os.path.exists(MODEL_FOLDER):
        print('Found existing ./models folder, skip creating a new one!')
        os.makedirs(MODEL_FOLDER, exist_ok=True)
    else:
        os.makedirs(MODEL_FOLDER)

    run_model()