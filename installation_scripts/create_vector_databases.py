"""
Script: create_vector_databases.py

This script processes pre-extracted manual page records to build faiss-based vector databases
for semantic search in the manual assistant application.

Workflow:
1. Loads and parses manual pages using RecordCreator.
2. Generates text chunks and metadata records from the input images.
3. Saves the records to disk for reuse (records.pkl).
4. Loads the records and splits them by manual.
5. For each manual:
    - Embeds the text chunks using a SentenceTransformer model.
    - Stores the embeddings and associated metadata in a FAISS vector database.

Usage:
    python create_vector_databases.py

Side Effects:
    - Creates or overwrites the vector_databases/ directory.

Note:
    This script is designed to be run after setting up the docs/ folder with structured manual images.
"""

if __name__ == '__main__':
    # Perform necessary imports
    import sys
    from pathlib import Path
    import os 
    base_folder = Path(__file__).resolve().parent.parent
    sys.path.append(str(base_folder))
    os.system('cls')
    print('🔄️ Preparing...')
    from classes.record_creator import RecordCreator
    from classes.task_generator import TaskGenerator
    from classes.embedder import Embedder
    from classes.vector_database import VectorDatabase
    from classes.db_creator import DbCreator
    import joblib
    from tqdm import tqdm
    import multiprocessing

    # Make sure a new python process is started for each worker
    # during multiprocessing
    multiprocessing.set_start_method('spawn', force=True)
    
    # Create the vector_databases folder, create records
    # and save them to this folder
    os.mkdir(base_folder / 'vector_databases')
    os.system('cls')
    print('🔄️ Creating metadata...')
    tasks = TaskGenerator(base_folder / 'docs').get_tasks()
    rc = RecordCreator(tasks)
    records = rc.create_records()
    joblib.dump(records, base_folder / 'vector_databases' / 'records.pkl')
    
    # Create the vector databases
    os.system('cls')
    print('🔄️ Creating vector databases...')
    records = joblib.load(base_folder / 'vector_databases'/ 'records.pkl')
    manual_names = list(set(list([record['manual'] for record in records])))
    DbCreator(records,manual_names).create_databases()
    
    # Celebrate
    os.system('cls')
    print('\n🎉 All done!')