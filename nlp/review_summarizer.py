import re
from typing import List, Iterable
from transformers import pipeline

class ReviewSummarizer:
    def __init__(self, model_name: str = "t5-small", device: int = 0, batch_size: int = 8):
        """
        model_name: Hugging Face model name (default 't5-small' for speed)
        device: 0 for GPU, -1 for CPU
        batch_size: number of inputs to process together on GPU
        """
        self.batch_size = batch_size
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=model_name,
            device=device
        )

        # ~250 words ≈ 512 tokens for t5-small
        self.word_limit = 250

    @staticmethod
    def clean_summary(text: str) -> str:
        """Clean model output."""
        if not text:
            return ""
        text = text.lower().strip()
        # Remove leading "<name>:"
        text = re.sub(r"^[a-z\s']{2,20}:\s*", "", text)
        text = re.sub(r"\s+", " ", text)                 # remove extra spaces
        text = re.sub(r"\s+([.,!?;:])", r"\1", text)      # fix space before punctuation
        return text.capitalize()

    def _prepare_text(self, reviews: List[str]) -> str:
        """Join and trim reviews for safe model input."""
        text = " ".join(r.strip() for r in reviews if r and r.strip())
        words = text.split()
        if len(words) > self.word_limit:
            text = " ".join(words[:self.word_limit])
        return f"summarize: {text}"

    def summarize_one(self, reviews: List[str]) -> str:
        """Summarize a single list of reviews."""
        if not reviews:
            return ""
        prompt = self._prepare_text(reviews)
        result = self.summarizer(
            prompt,
            max_new_tokens=50,
            do_sample=False
        )
        return self.clean_summary(result[0]["summary_text"])

    def summarize_many(self, list_of_reviews_lists: Iterable[List[str]]) -> List[str]:
        """Summarize multiple review lists in batches."""
        prompts = [self._prepare_text(rev) if rev else "" for rev in list_of_reviews_lists]
        outputs = self.summarizer(
            prompts,
            batch_size=self.batch_size,
            max_new_tokens=50,
            do_sample=False
        )
        return [self.clean_summary(o["summary_text"]) for o in outputs]
