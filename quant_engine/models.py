from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Decision(str, Enum):
    BUY = "BUY"
    WATCH = "WATCH"
    NO_TRADE = "NO_TRADE"


class Candidate(BaseModel):
    symbol: str
    as_of: datetime
    feature_values: dict[str, float | None] = Field(default_factory=dict)
    hard_failures: list[str] = Field(default_factory=list)
    evidence: dict[str, float] = Field(default_factory=dict)


class Prediction(BaseModel):
    symbol: str
    probability_target_before_stop: float = Field(ge=0, le=1)
    expected_return: float
    expected_loss: float
    risk_reward: float
    model_disagreement: float = Field(ge=0, le=1)
    data_quality: float = Field(ge=0, le=1)
    out_of_distribution: float = Field(ge=0, le=1)
    decision: Decision
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
