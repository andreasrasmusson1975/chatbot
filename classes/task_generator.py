"""
This module provides the TaskGenerator class for generating text extraction and record creation tasks
(refer to text_extractor.py and record_creator.py for details) for the contents of a folder containing 
subfolders with manual images (the docs folder - only visible after the installation scripts 
have been run).
"""

# Perform necessary imports 
from pathlib import Path

class TaskGenerator:
    """
    A class for generating text extraction and record creation tasks

    Attributes:
        data_dir (Path) - the path to the folder with manuals
        manual_folders (list) - a list of folder paths for each manual
    """
    def __init__(self,data_dir: str):
        # Set the data directory and initialize the manual_folders list
        self.data_dir = Path(data_dir)
        self.manual_folders = sorted([f for f in self.data_dir.iterdir() if f.is_dir()])
        
    def get_tasks(self) -> dict:
        """
        Creates and returns the tasks in the form of a dictionary.

        Returns
            dict: The dictionary of tasks

        """
        
        tasks={}
        # Iterate over the paths in manual_folders and add tasks to the
        # tasks dictionary.
        for manual_path in self.manual_folders:
            manual_path_str = str(manual_path)
            manual_name = manual_path.stem
            tasks[manual_name] = sorted((manual_path/Path('images')).glob('*.jpg'))
        return tasks