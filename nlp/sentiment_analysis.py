# sentiment_model_simple.py
from typing import List, Optional
import numpy as np
import torch
from sklearn.preprocessing import MinMaxScaler
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class SentimentModel:
    """
    Simple OOP wrapper to:
      - get sentiment scores for reviews
      - compute mean score
      - normalize mean score using MinMaxScaler
    """

    def __init__(
        self,
        model_name: str = "siebert/sentiment-roberta-large-english",
        device: int = 0,  # 0 = GPU, -1 = CPU
        max_len: int = 512,
        stride: int = 128,
    ):
        self.device = "cuda" if (device >= 0 and torch.cuda.is_available()) else "cpu"
        self.max_len = max_len
        self.stride = stride

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        dtype = torch.float16 if self.device == "cuda" else None
        self.model = (
            AutoModelForSequenceClassification.from_pretrained(
                model_name, torch_dtype=dtype
            )
            .to(self.device)
            .eval()
        )

    @torch.inference_mode()
    def get_scores(self, reviews: List[str]) -> List[Optional[float]]:
        """Returns P(positive) ∈ [0,1] for each review (None if invalid/empty)."""
        scores = []
        for text in reviews:
            if not isinstance(text, str) or not text.strip():
                scores.append(None)
                continue

            enc = self.tokenizer(
                text,
                truncation=True,
                max_length=self.max_len,
                stride=self.stride,
                return_overflowing_tokens=True,
                return_tensors=None,
            )

            logits_chunks = []
            for i in range(len(enc["input_ids"])):
                ids = torch.tensor(
                    [enc["input_ids"][i]], dtype=torch.long, device=self.device
                )
                attn = torch.tensor(
                    [enc["attention_mask"][i]], dtype=torch.long, device=self.device
                )
                with torch.autocast(
                    device_type="cuda", enabled=(self.device == "cuda")
                ):
                    logits = self.model(input_ids=ids, attention_mask=attn).logits
                logits_chunks.append(logits.float().cpu().numpy()[0])

            mean_logits = np.mean(logits_chunks, axis=0)
            m = float(mean_logits.max())
            probs = np.exp(mean_logits - m) / np.exp(mean_logits - m).sum()
            p_pos = float(probs[1])
            scores.append(p_pos)
        return scores

    @staticmethod
    def mean_score(scores: List[Optional[float]]) -> Optional[float]:
        """Return mean of valid scores, None if no valid entries."""
        vals = [s for s in scores if s is not None]
        return float(np.mean(vals)) if vals else None
