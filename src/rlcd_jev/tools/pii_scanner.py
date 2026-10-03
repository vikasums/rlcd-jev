"""
PII Detection Tool for Compliance Firewall.
"""

import re
from typing import List

PII_PATTERNS = [
    (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN'),
    (r'\b(?:\d[ -]*?){13,16}\b', 'CREDIT_CARD'),
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'EMAIL'),
    (r'\b(?:sk|api|key)(?:_[a-zA-Z0-9]+)*_[a-zA-Z0-9]{16,}\b', 'API_KEY')
]

def scan_pii(text: str) -> List[str]:
    """Scans text for PII entities (SSN, Credit Cards, Emails, API keys)."""
    found = []
    for pattern, label in PII_PATTERNS:
        if re.search(pattern, text):
            found.append(label)
    return found
