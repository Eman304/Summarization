import re
import nltk
from dataclasses import dataclass
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Download NLTK data
for pkg in ['punkt', 'wordnet', 'omw-1.4', 'punkt_tab']:
    nltk.download(pkg, quiet=True)

@dataclass
class SummarizerConfig:
    model_name: str = "facebook/bart-large-cnn"
    chunk_size: int = 250
    max_input: int = 1024
    max_output: int = 350
    min_output: int = 50
    num_beams: int = 6
    length_penalty: float = 1.0
    no_repeat_ngram_size: int = 3

class EnglishSummarizer:
    def __init__(self):
        self.config = SummarizerConfig()
        self.model, self.tokenizer = self.load_model()

    def load_model(self):
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_name)
            return model, tokenizer
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    def clean_text(self, text: str) -> str:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Input text must be a non-empty string.")
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^a-zA-Z0-9.,!?\' ]', '', text)
        return text.strip()

    def split_text(self, text: str, chunk_size: int = 400) -> list[str]:
        sentences = nltk.sent_tokenize(text)
        chunks, current_chunk, current_len = [], [], 0

        for sentence in sentences:
            word_count = len(sentence.split())
            if current_len + word_count > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk, current_len = [], 0
            current_chunk.append(sentence)
            current_len += word_count

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def postprocess_summary(self, text: str) -> str:
        sentences = nltk.sent_tokenize(text)
        seen, unique = set(), []
        for s in sentences:
            normalized = s.lower().strip()
            if normalized not in seen:
                seen.add(normalized)
                unique.append(s.strip())

        result = ' '.join(unique)
        result = re.sub(r'\s([?.!,])', r'\1', result)
        return result[0].upper() + result[1:] if result else result

    def summarize_chunks(self, chunks: list[str]) -> list[str]:
        summaries = []
        for chunk in chunks:
            try:
                inputs = self.tokenizer(
                    chunk,
                    return_tensors="pt",
                    max_length=self.config.max_input,
                    truncation=True,
                )
                summary_ids = self.model.generate(
                    inputs["input_ids"],
                    num_beams=self.config.num_beams,
                    max_length=self.config.max_output,
                    min_length=self.config.min_output,
                    length_penalty=self.config.length_penalty,
                    no_repeat_ngram_size=self.config.no_repeat_ngram_size,
                    early_stopping=True,
                )
                text = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                summaries.append(text)
            except Exception as e:
                print(f"Skipping chunk due to error: {e}")
        return summaries

    def summarize(self, text: str) -> str:
        cleaned = self.clean_text(text)
        chunks = self.split_text(cleaned, self.config.chunk_size)
        summaries = self.summarize_chunks(chunks)
        combined = " ".join(summaries)
        final = self.postprocess_summary(combined)
        return final