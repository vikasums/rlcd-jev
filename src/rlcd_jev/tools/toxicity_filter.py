"""
Toxicity and Harmful Content Scanner Tool.
"""

from typing import Tuple

TOXICITY_KEYWORDS = [
    'malware script',
    'ddos attack',
    'exploit vulnerability',
    'steal passwords',
    'unauthorized access'
]

def scan_toxicity(text: str) -> Tuple[int, float]:
    """
    Scans text for dangerous/toxic content triggers.
    Returns (hits, risk_score_contribution).
    """
    text_lower = text.lower()
    hits = sum(1 for kw in TOXICITY_KEYWORDS if kw in text_lower)
    score_contrib = 4.5 if hits > 0 else 0.0
    return hits, score_contrib
