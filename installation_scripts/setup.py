"""
Script: setup.py

This script automates the setup process for the PM209 dataset used in the manual assistant application. It performs the following tasks:

1. Downloads a ZIP archive of the PM209 dataset from Google Drive.
2. Extracts the archive to a local folder.
3. Copies all manual image subfolders to a local docs/ directory.
4. Downloads and saves the all-MiniLM-L6-v2 embedding model from the SentenceTransformers library.
5. Cleans up intermediate files and folders from the setup process.

Usage:
    python setup.py

Side Effects:
    - Creates the following directories (removing them if they already exist):
        - docs/: populated with manual image folders
        - models/: containing the downloaded embedding model
        - vector_databases/: removed during cleanup if present
    - Downloads a ZIP file (PM209.zip) and deletes it after extraction.

Note:
    This script is meant to be run as a standalone utility. It is not intended for import as a module.
"""


if __name__ == '__main__':
    # Perform necessary imports
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
    
    def download_from_google_drive(file_id: str, destination: Path):
        """
        Downloads a file from Google Drive using a file ID and saves it to a specified destination.

        Args:
            file_id (str): The unique identifier of the file on Google Drive.
            destination (Path): The local path where the file should be saved.
        """
        # Create a session and define the URL and parameters
        session = requests.Session()
        URL = "https://drive.usercontent.google.com/download"

        params = {
            "id": file_id,
            "export": "download",
            "confirm": "t"
        }
        # Create a get request for streaming
        response = session.get(URL, params=params, stream=True)
        # Find out the size of the file
        total_size = int(response.headers.get('content-length', 0))
        # Save the stream to disk
        with open(str(destination), "wb") as f, tqdm(
            total=total_size, unit='B', unit_scale=True, desc=str(destination)
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

    def unzip_file(zip_path: Path, extract_to=None):
        """
        Extracts the contents of a ZIP file to a specified directory.

        Args:
            zip_path (Path): Path to the .zip file to be extracted.
            extract_to (Path): 
                Target directory for extraction. 
                If None, contents will be extracted to a folder with the same name 
                as the ZIP file (without extension) in the same directory.
        """
        # Set the extract_to path and extract the file to that path
        if extract_to is None:
            extract_to = zip_path.parent / zip_path.stem  
        extract_to = Path(extract_to)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    def on_rm_error(func: callable, path: Path, exc_info: tuple):
        """
        Error handler for shutil.rmtree to forcefully delete read-only files.

        Args:
            func (callable): The function that raised the error.
            path (Path): The path that could not be removed.
            exc_info (tuple): Exception information returned by sys.exc_info().
        """
        # Change from readonly to writeable
        os.chmod(path, stat.S_IWRITE)
        # try the operation again.
        func(path)

    def delete_file_if_exists(file_path: Path):
        """
        Deletes a file if it exists.

        Args:
            file_path (Path): The path to the file that is to be deleted. 
        """
        if file_path.exists():
            file_path.unlink()
    
    def delete_folder_if_exists(path):
        """
        Deletes a folder (recursively) if it exists. If an error occurs,
        on_rm_error is called.
        """
        if path.exists() and path.is_dir():
            shutil.rmtree(path, onerror=on_rm_error)

    def copy_all_subfolders(src, dst):
        """
        Copies all subfolders from a source directory to a destination directory.

        Args:
            src (Path): Source directory containing subfolders to copy.
            dst (Path): Destination directory where subfolders will be copied.
        """
        # Iterate over the subfolders in the source folder and copy them to the
        # destination folder 
        for subfolder in src.iterdir():
            if subfolder.is_dir():
                target = dst / subfolder.name
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(subfolder, target)
    
    # Delete existing folders
    os.system('cls')
    print('🔄️ Preparing...')
    delete_folder_if_exists(base_folder / 'docs')
    delete_folder_if_exists(base_folder /'models')
    delete_folder_if_exists(base_folder /'vector_databases')
    
    # Download the PM209 dataset
    os.system('cls')
    print('🔄️ Downloading the PM209 dataset...')
    file_id = '1K6BPBYdTwKgA1OkNt_BUqVJAn3RDy59B'
    destination = base_folder / 'PM209.zip'
    download_from_google_drive(file_id, destination)
    
    # Extract the manuals
    os.system('cls')
    print('🔄️ Extracting manuals...')
    unzip_file(base_folder / 'PM209.zip')
    
    # Copy the manuals to the docs folder
    os.system('cls')
    print('🔄️ Creating and populating docs folder...')
    os.mkdir('docs')
    pm209_path = base_folder / 'PM209' / 'PM209' / 'images'
    copy_all_subfolders(pm209_path, base_folder / 'docs')

    # Download the all-MiniLM-L6-v2 model
    os.system('cls')
    print('🔄️ Downloading all-MiniLM-L6-v2 model...')
    SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2').save(str(base_folder / 'models' / 'all-MiniLM-L6-v2'))

    # Delete objects that are no longer needed
    os.system("cls")
    print('🔄️ Performing cleanup...')
    delete_file_if_exists(base_folder / 'PM209.zip')
    delete_folder_if_exists(base_folder / 'PM209')


