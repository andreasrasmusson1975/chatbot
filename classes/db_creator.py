"""
This module provides tools for creating vector databases for document retrieval.

It defines a DbCreator class that takes a list of preprocessed text chunks (records) 
and organizes them by manual name. For each manual, it uses an Embedder to generate
sentence embeddings and stores them in a VectorDatabase instance serialized to disk.

The embedding and vector database creation is parallelized using ProcessPoolExecutor 
for efficiency across multiple manuals.
"""

# Perform necessary imports
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from .vector_database import VectorDatabase
from .embedder import Embedder
import joblib
from pathlib import Path

def _process_manual(manual_name: str,records: list[dict]) -> str:
    """
    Processes all records associated with a given manual by generating embeddings
    and storing them in a vector database on disk.

    Args:
        manual_name (str): The name of the manual to process.
        records (list[dict]): A list of all available records. Each record should
                              be a dictionary containing at least a 'manual' key.

    Returns:
        str: The path to the saved vector database file for the given manual.
    """
    # Filter out the records associated with the manual
    manual_records = [record for record in records if record['manual'] == manual_name]
    # Create embeddings and initialize a VectorDatabase
    embeddings, manual_records = Embedder().encode(manual_records)
    vdb = VectorDatabase(dim=384)
    # Create the folder to stor the vector database in and the path to the file to save.
    base_dir = Path(__file__).resolve().parent.parent / "vector_databases" / manual_name
    base_dir.mkdir(parents=True, exist_ok=True)
    output_path = base_dir / "vdb.pkl"
    # Add embeddings to the vector database, save the vector database and
    # return the path of the vector database as a string
    vdb.add(embeddings, manual_records)
    joblib.dump(vdb, output_path)
    return str(output_path)

def _process_manual_star(args: tuple) -> str:
    """
    Unpacks arguments and delegates to the _process_manual function.

    This helper is used to enable argument unpacking when using 
    multiprocessing or concurrent execution patterns where the 
    mapping function only accepts a single argument.

    Parameters:
        args (tuple): A tuple containing (manual_name, records).

    Returns:
        str: Path to the saved vector database file for the manual.
    """
    return _process_manual(*args)

class DbCreator:
    """
    Creates and stores vector databases for each manual using parallel processing.

    This class takes a list of records and a list of manual names, filters the records
    by manual, generates embeddings using the Embedder, and stores them in
    corresponding VectorDatabase instances serialized to disk.

    Attributes:
        manual_names (list of str): Names of the manuals to process.
        records (list of dict): Record data, where each record contains at least a 'manual' field.
    """
    def __init__(self,records,manual_names):
        self.manual_names = manual_names
        self.records = records
    
    def create_databases(self):
        """
        Creates and saves vector databases for each manual in parallel.

        For each unique manual name in the dataset, this method filters the 
        relevant records, generates sentence embeddings, and stores them 
        in a dedicated VectorDatabase instance. The resulting databases are 
        saved as .pkl files under vector_databases/{manual_name}/vdb.pkl.

        Uses a process pool to parallelize database creation across manuals.

        Returns:
            DbCreator: The instance itself, to allow for method chaining.
        """
        manual_to_records = {}
        for record in self.records:            
            manual_to_records.setdefault(record['manual'], []).append(record)
        all_args = [(manual, records) for manual, records in manual_to_records.items()]

        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = executor.map(_process_manual_star, all_args)
            for result in tqdm(futures, total=len(all_args)):
                continue
    
        return self