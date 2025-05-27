# The manual assistant

## Introduction
This repo implements a a chatbot that answers questions about any of the 209 technical manuals in the PM209 dataset (https://github.com/AIM3-RUC/MPMQA). RAG-techiques are used for the implementation in the following way:

1. spaCy is used for tokenization and sentence splitting (https://spacy.io/)
2. Semantic chunking with overlap is implemented
3. Embeddings are performed using sentence transformers (https://www.sbert.net/)
4. Vector databases are implemented using faiss (https://github.com/facebookresearch/faiss)
5. The openai api is used for asking questions and receiving answers.

## Installation

### Dependencies

The following third-party software are needed:

1. A computer running windows.
2. An openai api key. It needs to be stored in an environment variable named "openai_api_key".
2. Tesseract
3. Microsoft Visual C++ Redistributable for Visual Studio 2015–2022 (x64)
4. Python 3.10.0

These will all (except of course the api key) be installed if you run install.bat.

### Installation procedure
Create the openai_api_key environment variable and then run the install.bat script: This script will:

1. Interactively install the Visual C++ Redistributalbe
2. Interactively install Python 3.10.0
3. Interactively install Tesseract 
4. Create an environment and install the packages in requirements.txt
5. Download the spaCy tokenizer and sentence splitter (en_core_web_sm)
6. Download the PM209 dataset and extract the manuals.
7. Download the all-MiniLM-L6-v2 model, used for embedding
8. Create vector databases for each of the manuals in the dataset.

It takes a while, even on a decent computer, so be patient

## Running the application
Simply run the run_app.bat script.