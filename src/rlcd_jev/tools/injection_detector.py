"""
Prompt Injection and Jailbreak Detector Tool.
"""

from typing import Tuple

PROMPT_INJECTION_KEYWORDS = [
    'ignore previous instructions',
    'disregard system prompt',
    'you are now in developer mode',
    'override safety rules',
    'system prompt:',
    'bypass security',
    'jailbreak',
    'do anything now'
]

def detect_prompt_injection(text: str) -> Tuple[int, float]:
    """
    Detects prompt injection triggers.
    Returns (keyword_hits, risk_score_contribution).
    """
    text_lower = text.lower()
    hits = sum(1 for kw in PROMPT_INJECTION_KEYWORDS if kw in text_lower)
    score_contrib = min(5.0, 3.0 + hits) if hits > 0 else 0.0
    return hits, score_contrib
