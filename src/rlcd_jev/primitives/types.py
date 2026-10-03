"""
Typed Primitives Module for System One (Jev RLCD) Decision Engine.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, TypeVar, Generic

T = TypeVar('T')

class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class Choice(Generic[T]):
    """Categorical decision primitive (Up to 255 predefined choices)."""
    selected: T
    options: List[T]
    confidence: float

    def is_confident(self, threshold: float = 0.90) -> bool:
        return self.confidence >= threshold


@dataclass
class Score:
    """Bounded numerical rating or ordered level primitive."""
    value: float
    min_value: float = 1.0
    max_value: float = 5.0
    level: RiskLevel = RiskLevel.LOW
    confidence: float = 1.0

    @classmethod
    def from_rating(cls, rating: float, max_val: float = 5.0, confidence: float = 0.95):
        ratio = rating / max_val
        if ratio < 0.25:
            lvl = RiskLevel.LOW
        elif ratio < 0.50:
            lvl = RiskLevel.MEDIUM
        elif ratio < 0.75:
            lvl = RiskLevel.HIGH
        else:
            lvl = RiskLevel.CRITICAL
        return cls(value=rating, max_value=max_val, level=lvl, confidence=confidence)


@dataclass
class Noul:
    """Binary / Boolean decision primitive with exact Brier-calibrated probability."""
    decision: bool
    probability: float
    proposition: str

    def exceeds_threshold(self, threshold: float = 0.90) -> bool:
        return self.probability >= threshold if self.decision else (1.0 - self.probability) >= threshold


@dataclass
class DecisionResult:
    """Container for multi-primitive parallel decision pass."""
    category: Choice[str]
    risk_score: Score
    is_threat: Noul
    latency_ms: float
    execution_path: str  # 'FAST_PASS', 'BLOCK_IMMEDIATE', 'SYSTEM_TWO_ESCALATE'
    details: Dict[str, Any] = field(default_factory=dict)
