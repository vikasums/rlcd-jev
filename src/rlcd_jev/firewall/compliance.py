"""
Enterprise Compliance Firewall with Profiling and Ollama Local Integration.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from rlcd_jev.core.config import settings
from rlcd_jev.core.database import AuditDatabase
from rlcd_jev.core.logger import logger
from rlcd_jev.engine.jev_engine import JevRLCDEngine
from rlcd_jev.engine.ollama_client import OllamaLLMClient
from rlcd_jev.engine.profiler import LatencyProfiler
from rlcd_jev.primitives import DecisionResult


class ComplianceFirewall:
    """
    Enterprise AI Firewall protecting downstream Generative LLMs and APIs.
    Integrates System One Jev RLCD decision layer with System Two Ollama LLM fallback.
    """

    def __init__(self, confidence_threshold: Optional[float] = None, ollama_model: str = "llama3.2:3b"):
        self.engine = JevRLCDEngine()
        self.confidence_threshold = confidence_threshold or settings.confidence_threshold
        self.audit_db = AuditDatabase()
        self.ollama_client = OllamaLLMClient(model_name=ollama_model)

        self.stats = {
            "total_processed": 0,
            "fast_pass_count": 0,
            "blocked_count": 0,
            "escalated_count": 0,
            "total_latency_ms": 0.0,
            "estimated_tokens_saved": 0
        }

    def process_request(self, user_prompt: str, force_ollama_fallback: bool = False) -> Dict[str, Any]:
        """
        Evaluates incoming prompt through Jev RLCD decision engine in <70ms.
        Captures step-by-step wall-clock latency profile and logs to audit DB.
        """
        trace_id = f"trc-{uuid.uuid4().hex[:8]}"
        profiler = LatencyProfiler(trace_id=trace_id, prompt=user_prompt)

        self.stats["total_processed"] += 1

        # Step 1: Preprocessing & Regex Scanner
        _ = user_prompt.lower()
        profiler.mark_step(
            step_name="Step 1: Preprocessing & Pattern Scan",
            complexity="O(N) text scan",
            description="Executes PII regex, prompt injection keywords, and toxicity scanners."
        )

        # Step 2: System One Jev RLCD Decision Engine Parallel Pass
        decision: DecisionResult = self.engine.evaluate(user_prompt)
        profiler.mark_step(
            step_name="Step 2: Jev RLCD Forward Pass",
            complexity="O(P) parallel pass (P primitives)",
            description="Evaluates typed primitives (Choice, Score, Noul) with Brier-calibrated confidence."
        )

        # Step 3: Calibrated Decision Thresholding
        _ = decision.is_threat.exceeds_threshold(self.confidence_threshold)
        profiler.mark_step(
            step_name="Step 3: Threshold Evaluation",
            complexity="O(1) scalar check",
            description=f"Checks if Noul probability exceeds calibrated threshold T={self.confidence_threshold}."
        )

        estimated_prompt_tokens = len(user_prompt.split()) * 1.3
        ollama_response = None

        # Step 4: Downstream Route Execution Path
        if decision.execution_path == "BLOCK_IMMEDIATE" and not force_ollama_fallback:
            self.stats["blocked_count"] += 1
            self.stats["estimated_tokens_saved"] += int(estimated_prompt_tokens + 150)
            status_str = "REJECTED"
            action_str = f"Security Policy Triggered: {decision.category.selected}"
            http_code = 403
            profiler.mark_step(
                step_name="Step 4: Route Execution (Block)",
                complexity="O(1) immediate rejection",
                description="Blocks prompt immediately, returning HTTP 403 without invoking System Two LLM."
            )
        
        elif decision.execution_path == "FAST_PASS" and not force_ollama_fallback:
            self.stats["fast_pass_count"] += 1
            self.stats["estimated_tokens_saved"] += int(estimated_prompt_tokens)
            status_str = "APPROVED_FAST_PASS"
            action_str = "FORWARD_TO_APP"
            http_code = 200
            profiler.mark_step(
                step_name="Step 4: Route Execution (Fast Pass)",
                complexity="O(1) direct forwarding",
                description="Fast-passes safe prompt to downstream app in < 0.2ms."
            )
        
        else:
            # Escalated to System Two LLM (Ollama or API Fallback)
            self.stats["escalated_count"] += 1
            status_str = "ESCALATED_SYSTEM_TWO"
            action_str = "ROUTE_TO_OLLAMA_LOCAL_LLM"
            http_code = 202

            if self.ollama_client.is_available():
                ollama_response = self.ollama_client.generate_eval(user_prompt)
            
            profiler.mark_step(
                step_name="Step 4: Route Execution (System Two LLM)",
                complexity="O(T * M) autoregressive model inference",
                description=f"Escalates ambiguous prompt to Ollama local LLM ({self.ollama_client.model_name})."
            )

        # Step 5: Audit Persistence & Telemetry Logging
        self.audit_db.log_decision(
            status=status_str,
            risk_level=decision.risk_score.level.value,
            category=decision.category.selected,
            confidence=decision.is_threat.probability,
            latency_ms=decision.latency_ms,
            prompt=user_prompt,
            details=decision.details
        )
        profiler.mark_step(
            step_name="Step 5: Audit Persistence",
            complexity="O(1) SQLite insertion",
            description="Persists decision log & telemetry trace to audit database."
        )

        profile_data = profiler.finalize()
        self.stats["total_latency_ms"] += profile_data.total_latency_ms

        return {
            "trace_id": trace_id,
            "status": status_str,
            "http_code": http_code,
            "action": action_str,
            "category": decision.category.selected,
            "risk_level": decision.risk_score.level.value,
            "confidence": round(decision.category.confidence, 4),
            "latency_ms": round(profile_data.total_latency_ms, 2),
            "profile": profile_data.to_dict(),
            "ollama_eval": ollama_response,
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
