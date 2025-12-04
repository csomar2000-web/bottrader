import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

class SentimentModel:
    def __init__(self, cfg):
        self.cfg = cfg
        self.tokenizer = AutoTokenizer.from_pretrained(cfg["model"])
        self.model = AutoModelForSequenceClassification.from_pretrained(cfg["model"])
        self.labels = [-1, 0, 1]

    def score(self, text):
        x = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            y = self.model(**x).logits.softmax(dim=1).squeeze().numpy()
        idx = int(np.argmax(y))
        return self.labels[idx], float(y[idx])
