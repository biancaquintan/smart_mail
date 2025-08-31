from __future__ import annotations
import joblib
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from .nlp import build_vectorizer
from .utils import is_short_or_random

LABELS = ["Improdutivo", "Produtivo"]

@dataclass
class EmailClassifier:
  pipeline: Pipeline

  @classmethod
  def new(cls) -> "EmailClassifier":
    vec = build_vectorizer()
    clf = LogisticRegression(max_iter=5000, C=1.0)
    pipe = Pipeline([
      ("tfidf", vec),
      ("clf", clf),
    ])
    return cls(pipe)

  @staticmethod
  def labels() -> list[str]:
    return LABELS

  def save(self, path: str) -> None:
    joblib.dump(self.pipeline, path)

  @classmethod
  def load(cls, path: str) -> "EmailClassifier":
    pipe = joblib.load(path)
    return cls(pipe)
    
  def predict_label(self, text: str) -> str:
    labels, _ = self.predict_proba_label([text])
    return labels[0]

  def predict_proba_label(self, texts: list[str]) -> tuple[list[str], list[float]]:
    labels = []
    probs = []

    for text in texts:
      # marcar como suspeito
      short_or_random = is_short_or_random(text)

      pred = self.pipeline.predict([text])[0]

      # normalizar pred para string
      if isinstance(pred, (int, bool)):
        label = LABELS[int(pred)]
      else:
        label = str(pred)

      prob_value = 1.0
      if hasattr(self.pipeline.named_steps["clf"], "predict_proba"):
        p = self.pipeline.predict_proba([text])[0]
        try:
          classes = list(self.pipeline.named_steps["clf"].classes_)
          if pred in classes:
            idx = classes.index(pred)
            prob_value = float(p[idx])
          elif isinstance(pred, (int, bool)) and int(pred) in classes:
            idx = classes.index(int(pred))
            prob_value = float(p[idx])
          elif str(pred) in classes:
            idx = classes.index(str(pred))
            prob_value = float(p[idx])
          else:
            prob_value = float(max(p))
        except Exception:
          prob_value = float(max(p))

      # Se texto curto/aleatório mas modelo considerar Produtivo com confiança alta,
      # respeita o modelo. Só força improdutivo quando confiança é muito baixa.
      if short_or_random and prob_value < 0.75:
        label = "Improdutivo"
        prob_value = 1.0

      labels.append(label)
      probs.append(prob_value)

    return labels, probs

