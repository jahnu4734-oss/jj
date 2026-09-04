from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import pandas as pd


class LookAheadError(ValueError):
    pass


def assert_point_in_time(observed_at: datetime, available_at: datetime) -> None:
    if available_at > observed_at:
        raise LookAheadError(
            f"Feature is not available at decision time: available_at={available_at!s} > observed_at={observed_at!s}"
        )


def validate_point_in_time_frame(frame: pd.DataFrame) -> None:
    required = {"observed_at", "available_at"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing timestamp columns: {sorted(missing)}")
    observed = pd.to_datetime(frame["observed_at"], utc=True)
    available = pd.to_datetime(frame["available_at"], utc=True)
    invalid = available > observed
    if invalid.any():
        first = frame.index[invalid][0]
        raise LookAheadError(f"Point-in-time violation at row {first}")


@dataclass(frozen=True)
class BacktestConfig:
    target_pct: float = 0.04
    stop_pct: float = 0.02
    max_holding_days: int = 5
    slippage_bps: float = 5.0
    fee_bps: float = 0.0


@dataclass(frozen=True)
class Outcome:
    outcome: str
    return_pct: float
    holding_days: int


def resolve_long_trade(
    entry_price: float,
    future_bars: pd.DataFrame,
    config: BacktestConfig,
) -> Outcome:
    """Conservative OHLC resolution: if target and stop hit in the same bar, assume stop first."""
    if entry_price <= 0:
        raise ValueError("entry_price must be positive")
    target = entry_price * (1 + config.target_pct)
    stop = entry_price * (1 - config.stop_pct)
    n = 0
    for _, bar in future_bars.head(config.max_holding_days).iterrows():
        n += 1
        high = float(bar["high"])
        low = float(bar["low"])
        if low <= stop and high >= target:
            return Outcome("LOSS_AMBIGUOUS", -config.stop_pct, n)
        if low <= stop:
            return Outcome("LOSS", -config.stop_pct, n)
        if high >= target:
            return Outcome("WIN", config.target_pct, n)
    return_pct = (float(future_bars.head(config.max_holding_days).iloc[-1]["close"]) / entry_price) - 1 if not future_bars.head(config.max_holding_days).empty else 0.0
    return Outcome("TIMEOUT", return_pct, n)
