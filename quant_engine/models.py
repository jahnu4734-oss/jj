from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Decision(str, Enum):
    BUY = "BUY"
    WATCH = "WATCH"
    NO_TRADE = "NO_TRADE"


class Observation(BaseModel):
    symbol: str
    observed_at: datetime
    available_at: datetime
    features: dict[str, float | None] = Field(default_factory=dict)

    def point_in_time_valid(self) -> bool:
        return self.available_at <= self.observed_at


class Candidate(BaseModel):
    symbol: str
    as_of: datetime
    feature_values: dict[str, float | None] = Field(default_factory=dict)
    hard_failures: list[str] = Field(default_factory=list)
    vetoes: list[str] = Field(default_factory=list)
    evidence: dict[str, float] = Field(default_factory=dict)
    confirmed_rules: int = 0
    data_quality: float = Field(default=0.0, ge=0, le=1)
    out_of_distribution: float = Field(default=1.0, ge=0, le=1)


class Prediction(BaseModel):
    symbol: str
    as_of: datetime | None = None
    probability_target_before_stop: float = Field(ge=0, le=1)
    expected_return: float
    expected_loss: float
    risk_reward: float = Field(ge=0)
    model_disagreement: float = Field(ge=0, le=1)
    data_quality: float = Field(ge=0, le=1)
    out_of_distribution: float = Field(ge=0, le=1)
    decision: Decision
    final_score: float = Field(ge=0, le=100)
    reasons: list[str] = Field(default_factory=list)


class BacktestTrade(BaseModel):
    symbol: str
    entry_time: datetime
    entry_price: float
    stop_price: float
    target_price: float
    exit_time: datetime | None = None
    exit_price: float | None = None
    outcome: str | None = None
    pnl_pct: float | None = None
