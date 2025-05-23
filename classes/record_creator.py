
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from .text_extractor import TextExtractor
from .semantic_chunker import SemanticChunker

def _process_page(task, path):
    extractor = TextExtractor(path)
    text = extractor.get_text()
    chunker = SemanticChunker()
    chunks = chunker.chunk(text)

    return [
        {
            "manual": task,
            "path": str(path),
            "chunk": i,
            "text": chunk
        }
        for i, chunk in enumerate(chunks)
    ]

def _process_page_star(args):
    return _process_page(*args)


class RecordCreator:
    def __init__(self, tasks):
        self.tasks = tasks

    def create_records(self):
        all_args = [(task, path) for task in self.tasks for path in self.tasks[task]]
        records = []

        with ProcessPoolExecutor() as executor:
            futures = executor.map(_process_page_star, all_args)
            for result in tqdm(futures, total=len(all_args)):
                records.extend(result)

        return sorted(records,key = lambda record: record['manual'])