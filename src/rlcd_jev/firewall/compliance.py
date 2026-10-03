"""
Enterprise Compliance Firewall Implementation.
"""

from typing import Dict, Any, List
from rlcd_jev.core.config import settings
from rlcd_jev.core.database import AuditDatabase
from rlcd_jev.core.logger import logger
from rlcd_jev.engine.jev_engine import JevRLCDEngine
from rlcd_jev.primitives import DecisionResult


class ComplianceFirewall:
    """
    Enterprise AI Firewall protecting downstream Generative LLMs and APIs.
    """

    def __init__(self, confidence_threshold: float = None):
        self.engine = JevRLCDEngine()
        self.confidence_threshold = confidence_threshold or settings.confidence_threshold
        self.audit_db = AuditDatabase()

        self.stats = {
            "total_processed": 0,
            "fast_pass_count": 0,
            "blocked_count": 0,
            "escalated_count": 0,
            "total_latency_ms": 0.0,
            "estimated_tokens_saved": 0
        }

    def process_request(self, user_prompt: str) -> Dict[str, Any]:
        """
        Evaluates incoming prompt through Jev RLCD decision engine in <70ms.
        Logs result to audit database.
        """
        self.stats["total_processed"] += 1
        decision: DecisionResult = self.engine.evaluate(user_prompt)
        
        self.stats["total_latency_ms"] += decision.latency_ms
        estimated_prompt_tokens = len(user_prompt.split()) * 1.3

        if decision.execution_path == "BLOCK_IMMEDIATE":
            self.stats["blocked_count"] += 1
            self.stats["estimated_tokens_saved"] += int(estimated_prompt_tokens + 150)
            status_str = "REJECTED"
            action_str = f"Security Policy Triggered: {decision.category.selected}"
            http_code = 403
        
        elif decision.execution_path == "FAST_PASS":
            self.stats["fast_pass_count"] += 1
            self.stats["estimated_tokens_saved"] += int(estimated_prompt_tokens)
            status_str = "APPROVED_FAST_PASS"
            action_str = "FORWARD_TO_APP"
            http_code = 200
        
        else:
            self.stats["escalated_count"] += 1
            status_str = "ESCALATED_SYSTEM_TWO"
            action_str = "ROUTE_TO_GPT4_OR_HUMAN"
            http_code = 202

        # Log decision to audit database in core/database.py
        self.audit_db.log_decision(
            status=status_str,
            risk_level=decision.risk_score.level.value,
            category=decision.category.selected,
            confidence=decision.is_threat.probability,
            latency_ms=decision.latency_ms,
            prompt=user_prompt,
            details=decision.details
        )

        return {
            "status": status_str,
            "http_code": http_code,
            "action": action_str,
            "category": decision.category.selected,
            "risk_level": decision.risk_score.level.value,
            "confidence": round(decision.category.confidence, 4),
            "latency_ms": round(decision.latency_ms, 2),
            "details": decision.details
        }

    def get_metrics(self) -> Dict[str, Any]:
        total = max(1, self.stats["total_processed"])
        avg_latency = self.stats["total_latency_ms"] / total
        cost_saved_usd = (self.stats["estimated_tokens_saved"] / 1000.0) * 0.01

        return {
            "total_requests": self.stats["total_processed"],
            "fast_pass_rate_pct": round((self.stats["fast_pass_count"] / total) * 100, 2),
            "blocked_rate_pct": round((self.stats["blocked_count"] / total) * 100, 2),
            "escalated_rate_pct": round((self.stats["escalated_count"] / total) * 100, 2),
            "avg_firewall_latency_ms": round(avg_latency, 2),
            "estimated_tokens_saved": self.stats["estimated_tokens_saved"],
            "estimated_cost_saved_usd": round(cost_saved_usd, 4)
        }
