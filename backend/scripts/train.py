import os
import logging
import pandas as pd
import nltk
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from app.model import EmailClassifier

logging.basicConfig(level=logging.INFO)

DEFAULT_DATA_PATH = "data/sample_email.csv"
DEFAULT_MODEL_PATH = "/models/model.joblib"

LABEL_MAP = {"Improdutivo": 0, "Produtivo": 1}

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

def load_data(path: str) -> pd.DataFrame:
  df = pd.read_csv(path)
  # Converte labels para inteiros
  df["label_int"] = df["label"].map(LABEL_MAP)
  return df

def train_and_evaluate(df: pd.DataFrame, model: EmailClassifier) -> None:
  X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["label_int"],
    test_size=0.2,
    random_state=42,
    stratify=df["label_int"]
  )

  model.pipeline.fit(X_train, y_train)
  y_pred = model.pipeline.predict(X_test)

  logging.info(
    "\nRelatório de classificação:\n%s",
    classification_report(y_test, y_pred, target_names=EmailClassifier.labels().values())
  )

def main() -> None:
  data_path = os.getenv("DATA_PATH", DEFAULT_DATA_PATH)
  model_path = os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH)

  df = load_data(data_path)
  model = EmailClassifier.new()

  train_and_evaluate(df, model)
  model.save(model_path)

  logging.info("✅ Modelo salvo em %s", model_path)

if __name__ == "__main__":
  main()
