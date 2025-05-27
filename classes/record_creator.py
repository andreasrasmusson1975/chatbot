"""
This module provides tools for creating structured records from document pages.

It defines a RecordCreator class that takes a dictionary mapping manual names to lists of file paths.
Each file is processed to extract text and semantically chunk it using TextExtractor and SemanticChunker.

The result is a list of records with manual name, file path, chunk index, and chunk text.
Processing is parallelized with ProcessPoolExecutor for efficiency.
"""

#Perform necessary imports
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from .text_extractor import TextExtractor
from .semantic_chunker import SemanticChunker
from pathlib import Path

def _process_page(task: str, path: Path) -> list[dict]:
    """
    Given the path of a manual page image, this function extracts
    the text from the image and splits the text into chunks using 
    semantic chunking.

    Args:
        tasks: (dict): A dictionary representing a task created with the class TaskCreator
        path: (Path): A path to a manual page image

    Returns:
        list[dict]: A list of chunk records, each with the following keys:
            - 'manual' (str): The name of the manual.
            - 'path' (str): The file path of the manual page as a string.
            - 'chunk' (int): The index of the chunk in the document.
            - 'text' (str): The content of the chunk.
    """
    # Extract the text from the image at the given path
    extractor = TextExtractor(path)
    text = extractor.text
    # Create chunks using semantic chunking
    chunker = SemanticChunker()
    chunks = chunker.chunk(text)
    # return a list a list of record dicts
    return [
        {
            'manual': task,
            'path': str(path),
            'chunk': i,
            'text': chunk
        }
        for i, chunk in enumerate(chunks)
    ]

def _process_page_star(args):
    return _process_page(*args)


class RecordCreator:
    """
    A class for processing a collection of chunking tasks created with the class
    TaskGenerator. Processing is parallelized for speed.

    """
    def __init__(self, tasks):
        self.tasks = tasks

    def create_records(self):
        """
        Processes all the chunking tasks in a task dictionary using the
        _process_page_star function. Processing is parallelized. 

        Returns:
            list - a list of records.
        """
        # Gather all (task,path) pairs in a long list and initialize the records list
        all_args = [(task, path) for task in self.tasks for path in self.tasks[task]]
        records = []

        # Parallelize the processing of each (task,path) pair in all_args
        # and add the results to records
        with ProcessPoolExecutor() as executor:
            futures = executor.map(_process_page_star, all_args)
            for result in tqdm(futures, total=len(all_args)):
                records.extend(result)
        # Return the records list, sorted by manual name
        return sorted(records,key = lambda record: record['manual'])