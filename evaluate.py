from classes.evaluator import Evaluator
from tqdm import tqdm
from pathlib import Path
import joblib
import pandas as pd
import os 
import random

def evaluate_manual(manual_name):
    try:
        ev = Evaluator(manual_name)
        joblib.dump(ev.evaluation_df,f'evaluation/{manual_name}.pkl')
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    os.system("cls")
    manual_names = [d.name for d in Path('vector_databases').iterdir() if d.is_dir()]
    random.shuffle(manual_names)

    completed = 0
    attempts = 0
    target = 100

    with tqdm(total=target, desc="Evaluating performance on manuals") as pbar:
        while manual_names and completed < target:
            manual_name = manual_names.pop()
            path = Path('.')/'evaluation'/f'{manual_name}.pkl'
            if not path.exists():
                success = evaluate_manual(manual_name)
            else:
                success = False
            attempts += 1
            if success:
                completed += 1
                pbar.update(1)
    print(f"\n🎯 Completed {completed} evaluations in {attempts} attempts.")



