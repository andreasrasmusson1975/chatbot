"""
A simple wrapper around a SentenceTransformer model for embedding text records.
"""
# Perform necessary imports
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

class Embedder:
    """
    This class loads a local SentenceTransformer model (by default 'all-MiniLM-L6-v2')
    and provides a method to convert batches of dictionary records into dense vector
    embeddings suitable for similarity search or downstream tasks.
    """
    def __init__(self):
        """
        Initializes the Embedder by loading a SentenceTransformer model from a local path.

        The model is expected to be located at 'models/all-MiniLM-L6-v2' relative to the project root.
        This local model is used to generate text embeddings via the SentenceTransformer library.
        """
        # Load the model
        model_path = Path(__file__).resolve().parent.parent/'models'/'all-MiniLM-L6-v2'
        self.model = SentenceTransformer(str(model_path))

    def encode(
        self,
        records: list[dict],
        text_key: str = 'text',
        batch_size: int = 32
    ) -> tuple:
        """
        Encodes a list of text records into dense vector embeddings using a SentenceTransformer model.

        Parameters:
            records (list[dict]): A list of dictionaries, each containing a text field to embed.
            text_key (str): The key in each dictionary that contains the text string to encode. Defaults to 'text'.
            batch_size (int): The number of texts to encode at once. Larger values may speed up encoding if memory allows.

        Returns:
            tuple[np.ndarray, list[dict]]: 
                - A NumPy array of shape (len(records), embedding_dim) containing the embeddings.
                - The original list of input records (unchanged), for convenience in downstream processing.
        """
        # Create a list of the texts that are to be encoded and then encode them
        texts = [record[text_key] for record in records]
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=False
        )
        embeddings = np.array(embeddings, dtype=np.float32)
        return embeddings, records
