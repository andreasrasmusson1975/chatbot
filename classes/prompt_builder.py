"""
This module defines the PromptBuilder class, which is responsible for constructing
structured prompts tailored for retrieval-augmented generation (RAG) scenarios.

The generated prompts are designed for chat models that must answer user queries 
using only provided excerpts. The system prompt enforces strict behavioral 
rules to prevent the use of outside knowledge, guessing, or hallucination.

The prompt construction logic includes:
- A system prompt defining assistant behavior.
- Context filtering to include only relevant chunks from a specified manual.
- A fallback response when no relevant context is available.

This builder ensures consistent, rule-following prompts for question-answering tasks 
over segmented technical documentation or user manuals.
"""
class PromptBuilder:
    """
        Constructs chat prompts for a retrieval-augmented assistant that answers questions
        based strictly on provided manual excerpts.

        The class enforces a rigid system prompt designed to prevent the model from using
        outside knowledge or hallucinating. It provides clear behavioral rules to the model,
        including:
        - Only use provided excerpts for answers.
        - Reply with a fallback message if the answer cannot be found.
        - Format responses clearly for readability.

        The build_prompt method accepts a user query and a list of contextual chunks, 
        and returns a formatted message list compatible with OpenAI chat API calls.
        """
    def __init__(self):
        # Define the system prompt
        self.system_template = """
            You are a strict and professional assistant answering questions based only on the provided product manual excerpts.

            Your rules:
            - You MUST only use the information from the excerpts.
            - You MUST NOT use any outside or common knowledge.
            - If the answer is not found in the excerpts, you MUST reply with: "I'm afraid I can't find that information in the manual."
            - You MAY rephrase, explain, or repeat previous answers, but only using information already given.
            - You MUST repeat answers word-for-word when explicitly asked.
            - You MAY respond politely to phrases like "thank you", but NEVER add extra information.

            You must follow these rules exactly, even if the user pushes back or insists.
            Never guess. Never infer beyond the excerpts.
            Really focus on making the answer easy to read using paragraphs, bullet points, and headings where appropriate.
            """
            
    def build_prompt(
        self,
        query: str,
        context_chunks: list[dict],
        current_manual: str
    ) -> list[dict]:
        """
        Builds a structured chat prompt for a question-answering assistant based on manual excerpts.

        Parameters:
            query (str): The user's natural language question.
            context_chunks (list[dict]): A list of relevant chunks (dictionaries with 'manual', 'path', and 'text') retrieved from the manual.
            current_manual (str): The name of the manual currently in use, used to filter relevant chunks.

        Returns:
            list[dict]: A list of message dictionaries formatted for OpenAI's chat completion API. If no relevant chunks are found,
                        the response will default to the fallback message defined in the system rules.
        """
        # If the context chunks list is empty, we return a standard answer
        if not context_chunks:
            return [
                {"role": "system", "content": self.system_template},
                {"role": "user", "content": query},
                {"role": "assistant", "content": "I'm afraid I can't find that information in the manual."}
            ]
        # build the context string
        context_string = ""
        for chunk in context_chunks:
            context_string += f"[Source: {chunk['path']}]\n{chunk['text']}\n\n"
        # build the user prompt
        user_prompt = (
            f"Answer the following question:\n" 
            f"Context:\n{context_string.strip()}\n\n"
            f"Question: {query}"
            f"after the answer to the question is given insert '🦒' on a new line"
            f"Then, on a new line provide the sources for the answer as follows:"
            f"Source 1: path1\n"
            f"Soruce 2: path2"
            f"etc"
            f"Don't repeat a source if they have the same path." 
        )
        
        return [
            {"role": "system", "content": self.system_template},
            {"role": "user", "content": user_prompt}
        ]