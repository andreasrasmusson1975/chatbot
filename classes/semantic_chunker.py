"""
This module provides the SemanticChunker class for splitting raw text into semantically coherent chunks.

It uses spacy to segment input text into sentences and tiktoken to count tokens according to a specified
OpenAI model. Sentences are grouped into overlapping chunks that do not exceed a configurable token limit,
making them suitable for embedding or LLM input.

The chunking logic ensures that chunks are contextually meaningful and overlap slightly to preserve continuity.
"""

import spacy
import tiktoken

class SemanticChunker:
    def __init__(
            self,
            max_tokens: int = 512, 
            overlap:int = 50, 
            model_name:str = 'gpt-4o-mini'
    ) -> list[str]:
        """
        Initializes a SemanticChunker instance for splitting text into token-bounded chunks.

        Args:
            max_tokens (int): The maximum number of tokens allowed per chunk. Default is 512.
            overlap (int): The approximate number of tokens to include from the end of the previous chunk
                in the beginning of the next, to maintain context. Default is 50.
            model_name (str): The name of the OpenAI model to use for token counting via tiktoken.
                This determines the tokenization strategy. Default is 'gpt-4o-mini'.
        """
        # Store parameters
        self.max_tokens = max_tokens
        self.overlap = overlap
        self.model_name = model_name
        # Initialize the tokenizer and sentence segmenter
        self.enc = tiktoken.encoding_for_model(model_name)
        self.nlp = spacy.load("en_core_web_sm")

    def chunk(self,text):
        """
        Splits input text into semantically coherent chunks based on sentence boundaries and token limits.

        This method first segments the input text into sentences using spacy, then groups the sentences into
        overlapping chunks such that the total number of tokens per chunk does not exceed max_tokens.
        If a sentence exceeds max_tokens on its own, it is skipped. Overlap between chunks is controlled
        by the overlap parameter to preserve context continuity across chunk boundaries.

        Args:
            text (str): The raw input text to be chunked.

        Returns:
            list[str]: A list of text chunks, each containing one or more sentences, suitable for embedding
                       or input into a language model.
        """
        # Split into sentences
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        # Initialize chunks list, current chunk list and current_tokens int.
        chunks = []
        current_chunk = []
        current_tokens = 0
        # Iterate over the sentences
        for sentence in sentences:
            # Get the number of tokens of the encoding of the current sentence
            sentence_tokens = len(self.enc.encode(sentence))
            # If this number is larger than max_tokens, we skip the sentence altogether.
            if sentence_tokens > self.max_tokens:
                continue
            # Otherwise, if the number of tokens so far plus the number of tokens in
            # the (encoding of) the current sentence exceeds max_tokens, we
            # join all sentences collected so far into a single string 
            if current_tokens + sentence_tokens > self.max_tokens:
                chunk = " ".join(current_chunk)
                chunks.append(chunk)
                # if overlap has been specified, we do the following:
                # 1. Initialize an overlap chunk and an overlap token counter
                # 2. Iterate in reversed order over the sentences in the 
                #    current chunk and do the following for each sentence:
                #      2.1 Check the number of tokens in the encoding of
                #          the current previous sentence
                #      2.2 If this number plus the number of overlap tokens added
                #          so far does not exceed the pre-specified number of 
                #          overlap tokens, we insert the currently scanned previous
                #          sentence into the first place in the overlap chunk and 
                #          increase the overlap token counter with the number of tokens 
                #          in the encoding of the current previous sentence.
                #      2.3 If 2.2 is not the case, we break the current loop so as not
                #          to exceed the pre-specified number of overlap tokens.
                #
                #  3. Set the current chunk to the overlap chunk and current tokens to
                #     overlap tokens
                # 
                # If instead overlap has not been specified, we simply reset the current
                # chunk current_tokens counter.

                if self.overlap > 0:
                    overlap_chunk = []
                    overlap_tokens = 0
                    for prev_sentence in reversed(current_chunk):
                        prev_tokens = len(self.enc.encode(prev_sentence))
                        if overlap_tokens + prev_tokens <= self.overlap:
                            overlap_chunk.insert(0, prev_sentence)
                            overlap_tokens += prev_tokens
                        else:
                            break
                    current_chunk = overlap_chunk
                    current_tokens = overlap_tokens
                # Otherwise, we reset current_chunk and current_tokens
                else:
                    current_chunk = []
                    current_tokens = 0
            # append the current chunk to the current_chunk list
            # and update current_tokens
            current_chunk.append(sentence)
            current_tokens += sentence_tokens
        # If current_chunk is not empty add it to the chunks list
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks