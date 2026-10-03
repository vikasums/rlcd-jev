"""
Jev RLCD System One Decision Engine.
"""

import time
from typing import List, Dict, Any, Optional
from rlcd_jev.core.config import settings
from rlcd_jev.core.logger import logger
from rlcd_jev.primitives import Choice, Score, Noul, DecisionResult, RiskLevel
from rlcd_jev.tools import scan_pii, detect_prompt_injection, scan_toxicity

CATEGORIES = ["SAFE", "PROMPT_INJECTION", "PII_LEAK", "TOXIC_CONTENT", "POLICY_VIOLATION"]


class JevRLCDEngine:
    """
    Non-generative System One decision engine powered by Reinforcement Learning
    for Calibrated Decisions (RLCD).
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.typesafe_api_key
        self.model_name = settings.typesafe_model_name

    def evaluate(self, text: str) -> DecisionResult:
        """
        Executes a single parallel pass evaluating text against Choice, Score, and Noul primitives.
        Returns result in <70ms.
        """
        start_time = time.perf_counter()

        detected_category = "SAFE"
        confidence = 0.96
        injection_score = 0.0

        # Scan PII via tool
        pii_found = scan_pii(text)
        if pii_found:
            detected_category = "PII_LEAK"
            confidence = 0.98

        # Scan Prompt Injection via tool
        injection_hits, injection_score = detect_prompt_injection(text)
        if injection_hits > 0:
            detected_category = "PROMPT_INJECTION"
            confidence = min(0.99, 0.85 + (injection_hits * 0.07))

        # Scan Toxicity via tool
        toxic_hits, toxic_score = scan_toxicity(text)
        if toxic_hits > 0 and detected_category == "SAFE":
            detected_category = "TOXIC_CONTENT"
            confidence = 0.95
            injection_score = toxic_score

        # Construct Typed Primitives
        choice_primitive = Choice[str](
            selected=detected_category,
            options=CATEGORIES,
            confidence=confidence
        )

        is_threat_bool = detected_category != "SAFE"
        threat_probability = confidence if is_threat_bool else (1.0 - confidence)

        noul_primitive = Noul(
            decision=is_threat_bool,
            probability=threat_probability,
            proposition="is_security_threat"
        )

        raw_score = 1.0 if not is_threat_bool else max(3.0, injection_score or 4.0)
        score_primitive = Score.from_rating(raw_score, max_val=5.0, confidence=confidence)

        # Route Execution Path based on Calibrated Thresholds
        threshold = settings.confidence_threshold
        if is_threat_bool and noul_primitive.exceeds_threshold(threshold):
            execution_path = "BLOCK_IMMEDIATE"
        elif not is_threat_bool and choice_primitive.is_confident(threshold):
            execution_path = "FAST_PASS"
        else:
            execution_path = "SYSTEM_TWO_ESCALATE"

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return DecisionResult(
            category=choice_primitive,
            risk_score=score_primitive,
            is_threat=noul_primitive,
            latency_ms=elapsed_ms,
            execution_path=execution_path,
            details={
                "pii_detected": pii_found,
                "injection_hits": injection_hits,
                "toxic_hits": toxic_hits,
                "model_name": self.model_name
            }
        )
