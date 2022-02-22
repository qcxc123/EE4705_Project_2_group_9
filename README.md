# EE4705 Project 2 Group 9: General Knowledge Education Dialogue Models

This repository was created for a module on Human-Robot Interaction. It contains the source code for two general knowledge education dialogue models created using [RetGen](https://github.com/dreasysnail/RetGen) and [Rasa](https://github.com/RasaHQ/rasa). They can be interacted with individually or jointly.
The RetGen model is a knowledge-grounded conversational model jointly trained on multi-turn dialogue and document retrieval.
The Rasa model is a task-oriented model which generates multiple-choice questions for a variety of subjects, accepts a number as an answer, and keeps track of score.
It also provides an explanation for the answer when available (for the science dataset).
The RetGen folder was forked from the RetGen repository and modified. There is no need to clone/fork the Rasa repository as it can be installed as a package.

## Environment
To run both models successfully, set up a virtual environment.
### Pycharm
1. Install Python 3.8 on your machine if it is not yet installed.
2. Create a new Pycharm project, and set the base interpreter to Python 3.8
3. Clone this repository into the project folder via
```bash
git clone https://github.com/qcxc123/EE4705_Project_2_group_9
```

4. Install the necessary packages via:
```bash
pip install -r requirements.txt
```
The version of pytorch installed assumes you have a cuda-compatible GPU.

## Trained Models
### RetGen
The trained models for RetGen can be downloaded from here (to be added). Place these in RetGen/dialogpt/models/RetGen.
### Rasa
The trained model for Rasa can be found in Rasa/models.

## Chat with models
### Joint RetGen and Rasa
To chat with the two models jointly, open 3 terminals.
In terminal 1:
```bash
rasa run actions
```
In terminal 2:
```bash
rasa run --enable-api
```
In terminal 3:
```bash
python joint_chatbot.py --model_name_or_path "./models/RetGen/" --load_checkpoint "./models/RetGen/reddit_generator.pkl" --max_history -2 --top_k 500 --generation_length 30
```
These commands will deploy the rasa chatbot and action servers on local endpoints as indicated in Rasa/endpoints.yml, and run the RetGen model in Python. You may chat with the models jointly in terminal 3. The default model is Rasa. Type "chat mode" to switch to RetGen, and "quiz mode" to switch back to Rasa.

### RetGen only
To chat with the RetGen model, use the chatbot.py script which was adapted from [DialoGPT2-Interact](https://github.com/andreamad8/DialoGPT2-Interact).
```bash
cd RetGen/dialogpt
python chatbot.py --model_name_or_path "./models/RetGen/" --load_checkpoint "./models/RetGen/reddit_generator.pkl" --generation_length 30 --max_history -2 --top_k 1
```
### Rasa only
To chat with the Rasa model, open two terminals.
In terminal 1:
```bash
rasa run actions
```
In terminal 2:
```bash
rasa shell
```
You may then chat with the Rasa model in terminal 2.

## Datasets
### RetGen
The dataset used in RetGen fine-tuning can be downloaded here (to be added). Place these in RetGen/data.

### Rasa
1. The .yml data used in Rasa training can be found in Rasa/data. Note that the data labels must also be indicated in Rasa/domain.yml.
2. The .json files in Rasa/data are not used in training, but are retrieved using Rasa/actions/actions.py. The science.json was obtained from the [SciQ dataset](https://allenai.org/data/sciq ). The other .json files were generated from [Ni's MCQ dataset](https://www3.cs.stonybrook.edu/~chni/post/mcq-dataset/), using MCQ/text_to_json.py

## Train your own models
### RetGen
To fine-tune a model with Google Colab:
(To be added)

To fine-tune a model with local 12GB single-card GPU (adapted from [RetGen](https://github.com/dreasysnail/RetGen)), run the following command without new line characters.
(To be edited)
```bash
python joint_training.py
     --model_name_or_path configs
     --init_checkpoint dialogpt/models/RetGen/reddit_generator.pkl
     --train_input_file data/reddit_train.db
     --eval_input_file data/reddit_test.txt 
     --output_dir output/joint_reddit
     --file_suffix joint_reddit
     --train_batch_size 2
     --gradient_accumulation_steps 2
     --eval_batch_size 2
     --num_optim_steps 16000
     --encoder_model_type ance_roberta
     --pretrained_model_cfg bert-base-uncased
     --model_file dialogpt/models/RetGen/reddit_retriever.pkl
     --ctx_file data/wiki.txt
     --num_shards 1
     --batch_size 128
     --n_docs 2
     --encoding
     --load_trained_model
```

### Rasa
You can add NLU training data in data/nlu.yml.
You can add dialogue flow training data in data/rules.yml and data/stories.yml.
Do not forget to update domain.yml with the intent and action labels.
You can edit the model parameters such as max_ngram, max_history and epochs in Rasa/config.yml.
To train a new model after modifying the .yml files:
```bash
rasa train
```
To train a new model interactively:
```bash
rasa interactive
```
This will run "rasa train" and then start a shell for interactive tuning, and update the .yml files after the session.
