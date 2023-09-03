# SpaceINDIA-Bot
A chatbot that answers queries of user based on space missions happened in 2023

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
