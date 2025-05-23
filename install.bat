call python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python installation_scripts\setup.py
python installation_scripts\create_vector_databases.py

