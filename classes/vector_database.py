import faiss
import numpy as np

class VectorDatabase:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings: np.ndarray, records: list[dict]):
        self.index.add(embeddings)
        self.metadata.extend(records)

    def search_manual(self, query_embedding: np.ndarray, manual_name: str, top_k: int = 5):
        indices = [i for i, meta in enumerate(self.metadata)]
        D, I = self.index.search(query_embedding, top_k)
        results = []
        for idx_list in I:
            batch = [self.metadata[indices[i]] for i in idx_list]
            results.append(batch)
        return results


