from __future__ import annotations
import joblib
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from .nlp import build_vectorizer

LABELS = {0: "Improdutivo", 1: "Produtivo"}

@dataclass
class EmailClassifier:
  pipeline: Pipeline

  @classmethod
  def new(cls) -> "EmailClassifier":
    vec = build_vectorizer()
    clf = LogisticRegression(max_iter=1000)
    pipe = Pipeline([
        ("tfidf", vec),
        ("clf", clf),
    ])
    return cls(pipe)

  @staticmethod
  def labels() -> dict[int, str]:
    return LABELS

  def save(self, path: str) -> None:
    joblib.dump(self.pipeline, path)

  @classmethod
  def load(cls, path: str) -> "EmailClassifier":
    pipe = joblib.load(path)
    return cls(pipe)

  def predict_proba_label(self, texts: list[str]) -> tuple[list[str], list[float]]:
    proba = None
    if hasattr(self.pipeline.named_steps["clf"], "predict_proba"):
        proba = self.pipeline.predict_proba(texts)
    preds = self.pipeline.predict(texts)
    labels = [LABELS[int(p)] for p in preds]
    probs = [float(max(p)) if proba is not None else 1.0 for p in (proba or [[1]] * len(preds))]
    return labels, probs
