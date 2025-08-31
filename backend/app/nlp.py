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

stemmed_stop_words = [_pt_stemmer.stem(w) for w in stop_words_pt]

def is_random_text(text: str) -> bool:
  """Detecta textos curtos ou aleatórios"""
  if len(text) == 0:
    return True
  non_alphabetic_ratio = len(re.findall(r'[^A-Za-zÀ-ÿ0-9\s]', text)) / len(text)
  return non_alphabetic_ratio > 0.8 or len(text) < 5

def tokenize(text: str) -> list[str]:
  """Tokeniza e aplica stem, ignora textos aleatórios"""
  if is_random_text(text):
    return []
  text = text.lower()
  parts = _token_simple.findall(text)
  return [_pt_stemmer.stem(p) for p in parts]

def build_vectorizer() -> TfidfVectorizer:
  """Constrói o vetor TF-IDF com tokenizer custom e stop words stemmizadas"""
  return TfidfVectorizer(
    tokenizer=tokenize,
    stop_words=stemmed_stop_words,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.9,
    token_pattern=None
  )
