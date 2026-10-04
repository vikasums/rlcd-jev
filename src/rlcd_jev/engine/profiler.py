"""
Microsecond Step-by-Step Latency Profiler for Pipeline Execution Tracing.
Captures individual phase timing, complexity metrics, and performance traces.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class StepTrace:
    step_name: str
    complexity: str
    duration_ms: float
    description: str

@dataclass
class ExecutionProfile:
    trace_id: str
    prompt_length_chars: int
    total_latency_ms: float
    steps: List[StepTrace] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "prompt_length_chars": self.prompt_length_chars,
            "total_latency_ms": round(self.total_latency_ms, 3),
            "step_breakdown": [
                {
                    "step": s.step_name,
                    "complexity": s.complexity,
                    "duration_ms": round(s.duration_ms, 3),
                    "pct_of_total": round((s.duration_ms / max(0.001, self.total_latency_ms)) * 100.0, 1),
                    "description": s.description
                }
                for s in self.steps
            ]
        }


class LatencyProfiler:
    """
    Step-by-step execution profiler providing transparent microsecond timing logs.
    """

    def __init__(self, trace_id: str, prompt: str):
        self.trace_id = trace_id
        self.prompt = prompt
        self.start_time = time.perf_counter()
        self.last_mark = self.start_time
        self.steps: List[StepTrace] = []

    def mark_step(self, step_name: str, complexity: str, description: str):
        now = time.perf_counter()
        duration_ms = (now - self.last_mark) * 1000.0
        self.last_mark = now
        self.steps.append(StepTrace(
            step_name=step_name,
            complexity=complexity,
            duration_ms=duration_ms,
            description=description
        ))

    def finalize(self) -> ExecutionProfile:
        total_latency_ms = (time.perf_counter() - self.start_time) * 1000.0
        return ExecutionProfile(
            trace_id=self.trace_id,
            prompt_length_chars=len(self.prompt),
            total_latency_ms=total_latency_ms,
            steps=self.steps
        )
