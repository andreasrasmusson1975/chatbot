if __name__ == '__main__':
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

    multiprocessing.set_start_method('spawn', force=True)
    
    os.mkdir(base_folder / 'vector_databases')
    os.system('cls')
    print('🔄️ Creating metadata...')
    tasks = TaskGenerator(base_folder / 'docs').get_tasks()
    rc = RecordCreator(tasks)
    records = rc.create_records()
    joblib.dump(records, base_folder / 'vector_databases' / 'records.pkl')
    
    os.system('cls')
    print('🔄️ Creating vector databases...')
    records = joblib.load(base_folder / 'vector_databases'/ 'records.pkl')
    manual_names = list(set(list([record['manual'] for record in records])))
    DbCreator(records,manual_names).create_databases()
    
    os.system('cls')
    print('\n🎉 All done!')