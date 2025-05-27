"""
This module provides the VectorDatabase class, which is a simple wrapper
around a faiss vector database for storage and retreival of vector 
embeddings together with associated metadata.
"""

# Perform necessary imports
import faiss
import numpy as np

class VectorDatabase:
    """
    This class implements a vector database for storage and retreival
    of vector embeddings together with associated metadata.

    Attributes:
        index (IndexFlatL2): A faiss index
        metadata (list): A list of metadata (records - see record_creator.py for details)
    """
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings: np.ndarray, records: list[dict]):
        """
        Adds embeddings and metadata to the database.

        Args:
            embeddings (str): A numpy array of embeddings
            records (list[dict]): a list of metadata in dictionary form 
        """
        self.index.add(embeddings)
        self.metadata.extend(records)

    def search_manual(self, query_embedding: np.ndarray, top_k: int = 5) -> list:
        """
        Searches the vector database for indices of text related to a user
        query embedding.

        Args:
            query_embedding (np.ndarray): A numpy array representation of an embedded query
            top_k (int): 
        """
        # Get the indices from the metadata
        indices = [i for i, meta in enumerate(self.metadata)]
        # Search the faiss index for indices with text related to the query
        # Return the five closest embeddings
        D, I = self.index.search(query_embedding, top_k)
        # Iterate over the returned indices and collect the corresponding
        # texts in the metadata.
        results = []
        for idx_list in I:
            batch = [self.metadata[indices[i]] for i in idx_list]
            results.append(batch)
        return results


