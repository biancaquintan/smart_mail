import io
import re
import math
from wordfreq import zipf_frequency
from pdfminer.high_level import extract_text

ALLOWED_TEXT_TYPES = {"text/plain", "application/pdf"}

FINANCE_KEYWORDS = [
  "pedido", "solicitação", "protocolo", "fatura", "boleto",
  "pagamento", "conta", "comprovante", "cartão", "financiamento"
]

def extract_text_from_pdf(file_bytes: bytes) -> str:
  with io.BytesIO(file_bytes) as fh:
    return extract_text(fh) or ""

def is_short_or_random(text: str) -> bool:
  text = text.strip()
  if len(text) < 15 or len(text.split()) < 3:
    return True

  words = [w.lower() for w in re.findall(r"\b[a-zA-Zá-úÁ-Ú]+\b", text)]
  numbers = re.findall(r"\d+", text)

  if numbers and any(kw in text.lower() for kw in FINANCE_KEYWORDS):
    return False

  non_alpha_ratio = sum(1 for c in text if not c.isalpha()) / max(1, len(text))
  if non_alpha_ratio > 0.4:
    return True

  vowel_ratios = [vowel_ratio(w) for w in words]
  if vowel_ratios and (sum(vowel_ratios) / len(vowel_ratios)) < 0.25:
    return True

  valid_words = [w for w in words if len(w) >= 3 and vowel_ratio(w) >= 0.25]
  if len(valid_words) == 0:
    return True

  rare_ratio = sum(1 for w in words if zipf_frequency(w, "pt") < 2.0) / len(words)
  if rare_ratio > 0.6:
    return True

  if len(set(words)) / max(1, len(words)) < 0.3:
    return True

  entropy = shannon_entropy(text)
  if entropy > 3.8:
    return True

  return False

def vowel_ratio(word: str) -> float:
  vowels = "aeiouáéíóúãõâêô"
  v = sum(1 for c in word.lower() if c in vowels)
  return v / len(word) if word else 0

def shannon_entropy(s: str) -> float:
  if not s:
    return 0.0
  freq = {}
  for c in s:
    freq[c] = freq.get(c, 0) + 1
  probs = [count / len(s) for count in freq.values()]
  return -sum(p * math.log2(p) for p in probs if p > 0)
