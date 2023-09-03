# SpaceINDIA-Bot for TextBase Titans Hackathon
A chatbot that answers queries of user based on space missions happened in 2023

## Features
1. Langchain integration: This chatbot chains various vectorstores that contain embeddings of text generated in 2023
2. Pinecone vectorstore: All data collected in 2023 is store in pinecone vectorstore to generate latest contexts for GPT-3.5
3. General knowledge about space missions held in 2023 covering Aditya L1, Chandrayaan-3 , James Webb telescope and more.

# Demo video

https://github.com/ADITYA964/SpaceINDIA-Bot/assets/61913852/c70e6b0b-7995-4310-964c-44df091216e4

## Description of folders and files
```tree
   SpaceINDIA-Bot
   |-- assets  
   |-- dist   
   |-- docs
   |-- examples
   |-- tests
   |-- textbase
   |-- PULL_REQUEST_TEMPLATE.md
   |-- README.md
   |-- main.py
   |-- poetry.lock
   |-- pyproject.toml
   |-- requirements.txt
```   

## Steps for bot inference

1. Clone this repository.
```shell
git clone https://github.com/ADITYA964/SpaceINDIA-Bot.git
```
2. Setup virtual python environment
```shell
pip install virtualenv

# Create environment
python -m venv test

.\test\Scripts\Activate.ps1
```
3. Setup poetry and install packages
```shell
pip install poetry

poetry shell

poetry install

pip install -r requirements.txt
```
4. Switch to working directory
```shell
cd .\SpaceINDIA-Bot\
```
5. Run SpaceINDIA bot on flask app
```shell
poetry run python textbase/textbase_cli.py test
``` 
6. Click server URL
```shell
Server URL: http://localhost:4000/
``` 
