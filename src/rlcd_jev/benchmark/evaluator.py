"""
System Two LLM Baseline Evaluator.
"""

import time
import random
from typing import Dict, Any
from rlcd_jev.core.config import settings


class SystemTwoLLMEvaluator:
    """
    Simulates standard heavy LLM (GPT-4 / Claude / LLaMA) compliance checking.
    Reads provider and model from core/config settings.
    """

    def __init__(self, cost_per_1k_tokens: float = 0.015):
        self.cost_per_1k_tokens = cost_per_1k_tokens
        self.provider = settings.system_two_provider
        self.model_name = settings.system_two_model_name

    def evaluate(self, text: str) -> Dict[str, Any]:
        start = time.perf_counter()
        
        simulated_latency = random.uniform(1.2, 2.2)
        time.sleep(simulated_latency)

        prompt_tokens = int(len(text.split()) * 1.3)
        generated_tokens = random.randint(120, 250)
        total_tokens = prompt_tokens + generated_tokens

        cost = (total_tokens / 1000.0) * self.cost_per_1k_tokens
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        return {
            "provider": self.provider,
            "model_name": self.model_name,
            "status": "EVALUATED_SYSTEM_TWO",
            "latency_ms": elapsed_ms,
            "tokens_used": total_tokens,
            "cost_usd": cost
        }
