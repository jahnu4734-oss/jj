from datetime import datetime, timezone
import pandas as pd
import pytest

from quant_engine.backtest import LookAheadError, assert_point_in_time, validate_point_in_time_frame, resolve_long_trade, BacktestConfig


def test_rejects_future_information() -> None:
    observed = datetime(2026, 1, 1, tzinfo=timezone.utc)
    available = datetime(2026, 1, 2, tzinfo=timezone.utc)
    with pytest.raises(LookAheadError):
        assert_point_in_time(observed, available)


def test_validates_frame() -> None:
    frame = pd.DataFrame({
        "observed_at": ["2026-01-01T09:30:00Z"],
        "available_at": ["2026-01-01T09:29:00Z"],
    })
    validate_point_in_time_frame(frame)


def test_same_bar_target_and_stop_is_conservative() -> None:
    bars = pd.DataFrame([{"high": 105.0, "low": 95.0, "close": 100.0}])
    outcome = resolve_long_trade(100.0, bars, BacktestConfig(target_pct=0.05, stop_pct=0.05))
    assert outcome.outcome == "LOSS_AMBIGUOUS"
    assert outcome.return_pct == pytest.approx(-0.05)
