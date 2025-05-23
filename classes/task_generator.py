from pathlib import Path

class TaskGenerator:
    def __init__(self,data_dir: str):
        self.data_dir = Path(data_dir)
        self.manual_folders = sorted([f for f in self.data_dir.iterdir() if f.is_dir()])
        
    def get_tasks(self):
        tasks={}
        for manual_path in self.manual_folders:
            manual_path_str = str(manual_path)
            manual_name = manual_path.stem
            tasks[manual_name] = sorted((manual_path/Path('images')).glob('*.jpg'))
        return tasks