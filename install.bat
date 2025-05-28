REM Install script for the application

REM Install tesseract
powershell -ExecutionPolicy Bypass -File .\installation_scripts\install_vc_redist.ps1
REM Install python 3.10.0
powershell -ExecutionPolicy Bypass -File .\installation_scripts\install_python.ps1

REM Install tesseract
powershell -ExecutionPolicy Bypass -File .\installation_scripts\install_tesseract.ps1
REM Create a python environment
call python -m venv env
REM Activate the environment
call env\Scripts\activate
REM Install packages according to requirements.txt
pip install -r requirements.txt
REM Download the spaCy en_core_web_sm model
python -m spacy download en_core_web_sm
REM Run the setup.py script
python installation_scripts\setup.py
REM Run the create_vector_databases.py script
python installation_scripts\create_vector_databases.py

