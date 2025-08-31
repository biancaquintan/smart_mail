import re
from typing import Iterable
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

_pt_stemmer = SnowballStemmer("portuguese")
_token_simple = re.compile(r"[A-Za-zÀ-ÿ0-9_-]+", re.UNICODE)

stop_words_pt = stopwords.words("portuguese")

custom_stopwords = {"na", "não", "sim", "com", "de", "para", "por", "a", "à", "o", "aos", "as", "e"}
stop_words_pt = stop_words_pt + list(custom_stopwords)

def is_random_text(text: str) -> bool:
  non_alphabetic_ratio = len(re.findall(r'[^A-Za-zÀ-ÿ0-9\s]', text)) / len(text)
  
  if non_alphabetic_ratio > 0.8:
    return True
  elif len(text) < 5:
    return True
  return False

def tokenize(text: str) -> list[str]:
  if is_random_text(text):
    return []
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
