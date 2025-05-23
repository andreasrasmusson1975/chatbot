import spacy
import tiktoken

class SemanticChunker:
    def __init__(self,max_tokens=512, overlap=50, model_name='gpt-3.5-turbo'):
        self.max_tokens = max_tokens
        self.overlap = overlap
        self.model_name = model_name
        self.enc = tiktoken.encoding_for_model(model_name)
        self.nlp = spacy.load("en_core_web_sm")

    def chunk(self,text):
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        chunks = []
        current_chunk = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = len(self.enc.encode(sentence))
            if sentence_tokens > self.max_tokens:
                continue
            if current_tokens + sentence_tokens > self.max_tokens:
                chunk = " ".join(current_chunk)
                chunks.append(chunk)

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
                else:
                    current_chunk = []
                    current_tokens = 0
            current_chunk.append(sentence)
            current_tokens += sentence_tokens
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks