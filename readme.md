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

The following third-party software needs to be installed:

1. A computer running windows.
2. An openai api key. It needs to be stored in an environment variable named "openai_api_key".
2. Tesseract (https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe)
3. Microsoft Visual C++ Redistributable for Visual Studio 2015–2022 (x64) (https://download.visualstudio.microsoft.com/download/pr/453680ea-b88a-411f-80fd-5db37fdc9dbb/5D9999036F2B3A930F83B7FE3E2186B12E79AE7C007D538F52E3582E986A37C3/VC_redist.x64.exe)
4. Python 3.10.0 (https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

### Installation procedure
Create the openai_api_key environment variable, install the dependencies above and then run the install.bat script: This script will:

1. Create an environment and install the packages in requirements.txt
2. Download the spaCy tokenizer and sentence splitter (en_core_web_sm)
3. Download the PM209 dataset and extract the manuals.
4. Download the all-MiniLM-L6-v2 model, used for embedding
5. Create vector databases for each of the manuals in the dataset.

It takes a while, even on a decent computer, so be patient

## Running the application
Simply run the run_app.bat script.