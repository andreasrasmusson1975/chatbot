"""
Module: manual_assistant

This module defines the ManualAssistant class, which facilitates sending user queries to
a gpt-4o-mini model via the OpenAI API 

Workflow:
1. Loads the vector database for the manual_name given as a parameter
2. Loads an embedder used for embedding user queries
3. Loads a prompt builder used to create the full prompt that is sent to the model.
4. An OpenAI client is initialized
5  The assistant is now ready to answer queries via the stream_user_query and 
   send_user_query methods
"""


# Perform necessary imports
from .vector_database import VectorDatabase
from .embedder import Embedder
from .prompt_builder import PromptBuilder
import os
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk
import joblib
from pathlib import Path
import numpy as np

class ManualAssistant:
    """
    A class for answering user questions based on a specific product manual using 
    semantic search and OpenAI's chat models.

    This assistant embeds the user's query, retrieves the most relevant text chunks 
    from a precomputed vector database of the manual, builds a prompt with context, 
    and sends it to an OpenAI model to generate a response. It supports both 
    streaming and standard synchronous responses.

    Attributes:
        manual_name (str): The name of the manual this assistant will use.
        vector_db (VectorDatabase): The loaded vector database for the manual.
        embedder (Embedder): Tool to generate embeddings for queries.
        prompt_builder (PromptBuilder): Constructs prompts with manual context.
        client (OpenAI): OpenAI client for model inference.
        model_name (str): Name of the OpenAI model used for completion.
        messages (list): Running conversation history for the chat.
    """
    def __init__(self,manual_name:  str,dim: int = 384):
        """
        Initializes the ManualAssistant with a given manual.

        Loads the corresponding vector database from disk, initializes the embedder 
        and prompt builder, and sets up the OpenAI client for question-answering.

        Args:
            manual_name (str): The name of the manual to associate with this assistant.
            dim (int, optional): Dimensionality of the embeddings used. Defaults to 384.
        """
        
        self.manual_name = manual_name
        # Load the vector database.
        db_path = Path(__file__).resolve().parent.parent / 'vector_databases' / manual_name / 'vdb.pkl'
        self.vector_db = joblib.load(db_path)
        # Initialize an ebedder, a prompt builder and the openai client.
        self.embedder = Embedder()
        self.prompt_builder = PromptBuilder()
        self.client = OpenAI(api_key=os.getenv('openai_api_key'))
        
        self.model_name = 'gpt-4o-mini'
        self.messages = []

    def stream_user_query(self, user_query: str):
        """
        Streams a model-generated response to a user query based on relevant manual content.

        This method:
        1. Encodes the user query into an embedding.
        2. Retrieves the top-k most relevant text chunks from the associated manual using a vector database.
        3. Constructs a prompt using these chunks and appends it to the ongoing message history.
        4. Sends the prompt to the OpenAI API with streaming enabled.
        5. Yields tokens incrementally as they are received from the model.
        6. Appends the full assistant response to the message history for future context.

        Parameters:
            user_query (str): The natural language question provided by the user.

        Yields:
            str: Individual tokens from the assistant's streamed response.
        """
        # Create the query embedding
        query_embedding, _ = self.embedder.encode([{"text": user_query}])
        query_embedding = np.array(query_embedding, dtype=np.float32)
        
        # Get the top five manual text chunks related to the query 
        top_chunks = self.vector_db.search_manual(query_embedding,5)[0]
        # Build the prompt and add it to the messages produced so far
        new_prompt = self.prompt_builder.build_prompt(user_query, top_chunks, current_manual=self.manual_name)
        if not self.messages:
            self.messages.append(new_prompt[0])
        self.messages.append(new_prompt[1])

        if not len(new_prompt) == 3:
            # Send the prompt (full message history actually) to the model and make sure it streams the result back
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.messages,
                temperature=0.0,
                stream=True,
            )
            # Iterate over the chunks in the stream and yield them one by one.
            # Also, save the full text to the messages list.
            full_text = ""
            for chunk in stream:
                if isinstance(chunk, ChatCompletionChunk):
                    delta = chunk.choices[0].delta
                    token = delta.content or ""
                    full_text += token
                    yield token

            self.messages.append({"role": "assistant", "content": full_text})
        else:
            yield new_prompt[2]['content']
            self.messages.append(new_prompt[2])
    
    def send_user_query(self,user_query: str) -> str:
        """
        Sends a user query to the model and returns the full assistant response.

        This method:
        1. Encodes the user query into an embedding vector.
        2. Retrieves the top-k most relevant manual chunks using a vector similarity search.
        3. Constructs a prompt using the query and retrieved chunks, and appends it to the conversation history.
        4. Sends the entire message history to the OpenAI API to get a non-streamed assistant response.
        5. Appends the assistant's reply to the message history.
        
        Parameters:
            user_query (str): The natural language question posed by the user.

        Returns:
            str: The assistant's full response as a string.
        """
        # Create the query embedding
        query_embedding, _ = self.embedder.encode([{"text": user_query}])
        query_embedding = np.array(query_embedding, dtype=np.float32)
        # Get the top five manual text chunks related to the query 
        top_chunks = self.vector_db.search_manual(query_embedding, self.manual_name, top_k=5)[0]
        # Build the prompt and add it to the messages produced so far
        prompt = self.prompt_builder.build_prompt(user_query, top_chunks, current_manual=self.manual_name)
        if not self.messages:
            self.messages.append(prompt[0])
        self.messages.append(prompt[1])
        if not len(prompt) == 3:
            # Send the prompt (full message history actually) to the model.
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.messages,
                temperature=0.0
            )
            # Extract the reply, add it to the messages list and return it
            assistant_reply = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": assistant_reply})
        else:
            assistant_reply = prompt[2]['content']
            self.messages.append(prompt[2])

        return assistant_reply