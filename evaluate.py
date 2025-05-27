"""
Script: evaluate_manuals.py

This script evaluates the performance of the assistant on a random subset of manuals
by generating and saving evaluation DataFrames for each manual using the Evaluator class.

Workflow:
    1. Retrieves all available manual names from the 'vector_databases/' directory.
    2. Randomly shuffles the manual list.
    3. Attempts to evaluate up to 100 manuals:
        - For each manual not yet evaluated (i.e., no .pkl file exists in 'evaluation/'),
          an Evaluator is instantiated.
        - The resulting evaluation DataFrame is saved as a .pkl file under 'evaluation/'.
        - Progress is shown via a tqdm progress bar.
    4. Reports the number of successful evaluations and total attempts at the end.

Usage:
    python evaluate_manuals.py

Side Effects:
    - Creates or updates files in the 'evaluation/' directory.

Note:
    The script is designed so that it can be run several times until all 209 manuals have
    been evaluated.
"""

# Perform necessary imports
from classes.evaluator import Evaluator
from tqdm import tqdm
from pathlib import Path
import joblib
import pandas as pd
import os 
import random

def evaluate_manual(manual_name):
    """
    Evaluates a single manual and saves the resulting evaluation DataFrame.

    Args:
        manual_name (str): Name of the manual to evaluate. Must correspond to a 
            valid subdirectory in 'vector_databases/'.

    Returns:
        bool: True if evaluation and saving succeeded, False if an exception occurred.

    Notes:
        - Saves the evaluation result to 'evaluation/<manual_name>.pkl'.
        - Exceptions are caught and suppressed; failure returns False.
        - Assumes the 'evaluation/' directory already exists.
    """    
    try:
        # Define an Evaluator object based on the manual_name given
        # This object takes care of the full evaluation for us-
        ev = Evaluator(manual_name)
        # Get the evaluation df and save it to disk
        joblib.dump(ev.evaluation_df,f'evaluation/{manual_name}.pkl')
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    os.system("cls")
    # Get and shuffle the manual names
    manual_names = [d.name for d in Path('vector_databases').iterdir() if d.is_dir()]
    random.shuffle(manual_names)
    # A few helper variables
    completed = 0
    attempts = 0
    target = 100
    # Iterate over the manual names
    with tqdm(total=target, desc="Evaluating performance on manuals") as pbar:
        while manual_names and completed < target:
            # Get and remove a manual name from the list
            manual_name = manual_names.pop()
            # Set the save path
            path = Path('.')/'evaluation'/f'{manual_name}.pkl'
            # If the file doesn't already exist, perform an evaluation
            if not path.exists():
                success = evaluate_manual(manual_name)
            else:
                success = False
            attempts += 1
            if success:
                completed += 1
                pbar.update(1)
    print(f"\n🎯 Completed {completed} evaluations in {attempts} attempts.")



