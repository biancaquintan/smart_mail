import re
from typing import Iterable
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

_pt_stemmer = SnowballStemmer("portuguese")
_token_simple = re.compile(r"[A-Za-zÀ-ÿ0-9_-]+", re.UNICODE)

stop_words_pt = stopwords.words("portuguese")

def tokenize(text: str) -> list[str]:
  text = text.lower()
  parts = _token_simple.findall(text)
  return [_pt_stemmer.stem(p) for p in parts]

def build_vectorizer() -> TfidfVectorizer:
  return TfidfVectorizer(
    tokenizer=tokenize,
    stop_words=stop_words_pt,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.9,
  )
