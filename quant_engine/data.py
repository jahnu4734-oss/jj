from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import pandas as pd

from .backtest import validate_point_in_time_frame


class MarketDataSource(ABC):
    """Adapter boundary for NSE/vendor/broker data without coupling research to one feed."""

    @abstractmethod
    def historical(self, symbols: list[str], start: datetime, end: datetime, interval: str) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def corporate_actions(self, symbols: list[str], start: datetime, end: datetime) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def derivatives(self, symbols: list[str], start: datetime, end: datetime, interval: str) -> pd.DataFrame:
        raise NotImplementedError


class PointInTimeDataset:
    def __init__(self, frame: pd.DataFrame):
        validate_point_in_time_frame(frame)
        self.frame = frame.copy()

    def as_of(self, when: datetime) -> pd.DataFrame:
        observed = pd.to_datetime(self.frame["observed_at"], utc=True)
        available = pd.to_datetime(self.frame["available_at"], utc=True)
        mask = (observed <= pd.Timestamp(when, tz="UTC")) & (available <= pd.Timestamp(when, tz="UTC"))
        return self.frame.loc[mask].copy()


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    return out


def require_columns(frame: pd.DataFrame, required: set[str]) -> None:
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"Missing required market-data columns: {missing}")
