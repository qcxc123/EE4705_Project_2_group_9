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

## Trained Model Links
### TA provide model
Our model retrained on filtered subreddit data can be downloaded from [here](https://drive.google.com/file/d/1Wb9qJoua_pZz_nOFsCeEYBPySpN6IMPE/view?usp=sharing).

### RetGen
Our fine-tuned model for RetGen can be downloaded from [here](https://drive.google.com/file/d/1-ySMdWy-GN82H9J2pD9PP1kQoWwaITCU/view?usp=sharing). Place the downloaded file in RetGen/dialogpt/models/RetGen. The model was fine-tuned using the [released RetGen Reddit retriever and generator](https://github.com/dreasysnail/RetGen).
### Rasa
Our trained model for Rasa can be found in Rasa/models.

## Chat with models
### Joint RetGen and Rasa
To chat with the two models jointly, open 3 terminals.
In terminal 1:
```bash
cd Rasa
rasa run actions
```
In terminal 2:
```bash
cd Rasa
rasa run --enable-api
```
In terminal 3:
```bash
cd RetGen/dialogpt
python joint_chatbot.py --model_name_or_path "./models/RetGen/" --load_checkpoint "./models/RetGen/reddit_generator.pkl" --max_history -2 --top_k 500 --generation_length 30
```
These commands will deploy the rasa chatbot and action servers on local endpoints as indicated in Rasa/endpoints.yml, and run the RetGen model in Python. You may chat with the models jointly in terminal 3. The default model is Rasa. Type "chat mode" to switch to RetGen, and "quiz mode" to switch back to Rasa.

### RetGen only
To chat with the RetGen model, run the batch file *run.bat*, or use our chatbot.py script which was adapted from [DialoGPT2-Interact](https://github.com/andreamad8/DialoGPT2-Interact).
```bash
cd RetGen/dialogpt
python chatbot.py --model_name_or_path "./models/RetGen/" --load_checkpoint "./models/RetGen/reddit_generator.pkl" --generation_length 30 --max_history -2 --top_k 1
```
### Rasa only
To chat with the Rasa model, open two terminals.
In terminal 1:
```bash
cd Rasa
rasa run actions
```
In terminal 2:
```bash
cd Rasa
rasa shell
```
You may then chat with the Rasa model in terminal 2.

## Datasets
### RetGen
The formatted arXiv dataset used in RetGen fine-tuning can be downloaded here (to be added). This was formatted from the raw released arXiv data. Download the Wiki data from the [RetGen repo](https://github.com/dreasysnail/RetGen). Place the datasets in RetGen/data.

### Rasa
1. The .yml data used in Rasa training can be found in Rasa/data. Note that the data labels must also be indicated in Rasa/domain.yml.
2. The .json files in Rasa/data are not used in training, but are retrieved using Rasa/actions/actions.py. The science.json was obtained from the [SciQ dataset](https://allenai.org/data/sciq ). The other .json files were generated from [Ni's MCQ dataset](https://www3.cs.stonybrook.edu/~chni/post/mcq-dataset/), using MCQ/text_to_json.py

## Train your own models
### RetGen
To fine-tune a model with Google Colab Pro's high RAM (26GB) GPU:
1. Create a Colab workspace with the notebook.ipynb and two folders "models" and "data".
2. In the "data" folder, download and place these two files inside: [wiki.txt](https://yizzhang.blob.core.windows.net/gdpt/RetGen_local/data/wiki.txt?sv=2019-10-10&st=2021-10-27T22%3A08%3A54Z&se=2025-10-28T22%3A08%3A00Z&sr=b&sp=r&sig=lfJIG1Is5i6XnWmbbyg3HcjFsL4ssNIfJygzf6OGnwI%3D) (2.5GB), [arxiv_train.tsv](https://drive.google.com/file/d/17RKwIEisJPspZfUsuVoD4Uw9glH2yL3o/view?usp=sharing) (2.17GB)
3. In the "models" folder, download and place the models you want to evaluate. The model trained in this project can be found under section **"Trained Models"**; the original RetGen checkpoints can be found in their [Github page](https://github.com/dreasysnail/RetGen).
4. Run the *notebook.ipynb*. Note that the **"Preprocess"** tab need only be run once to generate the train db.

To fine-tune a model with local single-card GPU (a RAM size of at least 20GB is highly recommended) (adapted from [RetGen](https://github.com/dreasysnail/RetGen)):
1. Install the apex and fairseq dependencies in your environment.
```
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
```
```
git clone https://github.com/pytorch/fairseq
cd fairseq
pip install --editable ./
```
2. In the "RetGen/data" folder, download and place these two files inside: [wiki.txt](https://yizzhang.blob.core.windows.net/gdpt/RetGen_local/data/wiki.txt?sv=2019-10-10&st=2021-10-27T22%3A08%3A54Z&se=2025-10-28T22%3A08%3A00Z&sr=b&sp=r&sig=lfJIG1Is5i6XnWmbbyg3HcjFsL4ssNIfJygzf6OGnwI%3D) (2.5GB), [arxiv_train.tsv](https://drive.google.com/file/d/17RKwIEisJPspZfUsuVoD4Uw9glH2yL3o/view?usp=sharing) (2.17GB)
3. Create a directory "RetGen/models" for any model checkpoints.
4. When training for the first time, preprocess the train.tsv by running this command. \
```python dialogpt/prepro.py --corpus data/arxiv_train.tsv --max_seq_len 512```
5. Run the shell script *run.sh* with updated paths. A *batch_size* of 8 and *num_shards* of 100 if recommended for a lower-end GPU (less than 26GB).

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
