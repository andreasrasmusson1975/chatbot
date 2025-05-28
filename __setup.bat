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