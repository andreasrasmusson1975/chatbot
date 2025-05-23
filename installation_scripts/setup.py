if __name__ == '__main__':
    import sys
    from pathlib import Path
    base_folder = Path(__file__).resolve().parent.parent
    sys.path.append(str(base_folder))

    import requests
    from tqdm import tqdm
    import zipfile
    import shutil
    import os
    import stat
    from sentence_transformers import SentenceTransformer
    
    def download_from_google_drive(file_id, destination):
        session = requests.Session()
        URL = "https://drive.usercontent.google.com/download"

        params = {
            "id": file_id,
            "export": "download",
            "confirm": "t"
        }

        response = session.get(URL, params=params, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(str(destination), "wb") as f, tqdm(
            total=total_size, unit='B', unit_scale=True, desc=str(destination)
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

    def unzip_file(zip_path, extract_to=None):
        if extract_to is None:
            extract_to = zip_path.parent / zip_path.stem  
        extract_to = Path(extract_to)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    def on_rm_error(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def delete_file_if_exists(file_path):
        if file_path.exists():
            file_path.unlink()
    
    def delete_folder_if_exists(path):
        if path.exists() and path.is_dir():
            shutil.rmtree(path, onerror=on_rm_error)

    def copy_all_subfolders(src, dst):
        for subfolder in src.iterdir():
            if subfolder.is_dir():
                target = dst / subfolder.name
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(subfolder, target)
    
    os.system('cls')
    print('🔄️ Preparing...')
    delete_folder_if_exists(base_folder / 'docs')
    delete_folder_if_exists(base_folder /'models')
    delete_folder_if_exists(base_folder /'vector_databases')

    os.system('cls')
    print('🔄️ Downloading the PM209 dataset...')
    file_id = '1K6BPBYdTwKgA1OkNt_BUqVJAn3RDy59B'
    destination = base_folder / 'PM209.zip'
    download_from_google_drive(file_id, destination)
    
    os.system('cls')
    print('🔄️ Extracting manuals...')
    unzip_file(base_folder / 'PM209.zip')
    
    os.system('cls')
    print('🔄️ Creating and populating docs folder...')
    os.mkdir('docs')
    pm209_path = base_folder / 'PM209' / 'PM209' / 'images'
    copy_all_subfolders(pm209_path, base_folder / 'docs')

    os.system('cls')
    print('🔄️ Downloading all-MiniLM-L6-v2 model...')
    SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2').save(str(base_folder / 'models' / 'all-MiniLM-L6-v2'))

    os.system("cls")
    print('🔄️ Performing cleanup...')
    delete_file_if_exists(base_folder / 'PM209.zip')
    delete_folder_if_exists(base_folder / 'PM209')


