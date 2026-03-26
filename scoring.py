# scoring.py
import re
import unicodedata
from difflib import SequenceMatcher

def normalize_text(s: str) -> str:
    """
    Normaliza texto para comparación:
    - minúsculas
    - elimina tildes/diacríticos
    - deja solo letras/espacios (incluye ñ)
    - colapsa espacios
    """
    s = (s or "").lower().strip()
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")  # quita tildes
    s = re.sub(r"[^a-zñ\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def similarity_percent(expected: str, predicted: str) -> float:
    e = normalize_text(expected)
    p = normalize_text(predicted)
    if not e and not p:
        return 100.0
    if not e or not p:
        return 0.0
    return round(SequenceMatcher(None, e, p).ratio() * 100, 2)

def label_score(score: float, ok: float = 90.0, partial: float = 70.0) -> str:
    if score >= ok:
        return "OK"
    if score >= partial:
        return "PARCIAL"
    return "NO"