"""
Real Microsoft Presidio Analyzer Engine Evaluator.
Executes live local presidio_analyzer.AnalyzerEngine() scans on your Mac workstation.
No simulation or fallback data.
"""

import time
from typing import Dict, Any, List
from rlcd_jev.core.logger import logger

try:
    from presidio_analyzer import AnalyzerEngine
    PRESIDIO_AVAILABLE = True
except ImportError:
    PRESIDIO_AVAILABLE = False


class LivePresidioEvaluator:
    """
    Live Microsoft Presidio Evaluator running presidio-analyzer natively on Mac.
    """

    def __init__(self):
        if not PRESIDIO_AVAILABLE:
            raise RuntimeError("presidio-analyzer is not installed in current Python environment.")
        self.analyzer = AnalyzerEngine()

    def evaluate(self, text: str) -> Dict[str, Any]:
        """
        Executes a live Microsoft Presidio analysis scan over text.
        Measures real wall-clock latency (ms) and returned PII entities.
        """
        start_time = time.perf_counter()

        # Execute live Presidio Analyzer scan
        results = self.analyzer.analyze(
            text=text,
            entities=["US_SSN", "CREDIT_CARD", "EMAIL_ADDRESS", "PHONE_NUMBER", "IP_ADDRESS"],
            language="en"
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        entities_found = [
            {
                "type": r.entity_type,
                "score": round(r.score, 4),
                "start": r.start,
                "end": r.end
            }
            for r in results
        ]

        has_pii = len(entities_found) > 0

        return {
            "engine": "Microsoft Presidio Analyzer (Live Local)",
            "has_pii": has_pii,
            "entities_found": entities_found,
            "latency_ms": round(elapsed_ms, 2)
        }
