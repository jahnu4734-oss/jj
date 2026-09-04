from datetime import datetime, timezone

from quant_engine.pipeline import evaluate
from quant_engine.scoring import score_candidate
from quant_engine.models import Decision


def good_features() -> dict[str, float | None]:
    return {
        "universe_nifty200": 1, "avg_volume_20d": 1_000_000,
        "promoter_holding_pct": 0.52, "risk_reward": 2.5,
        "turnover_cr": 100, "spread_pct": 0.001, "market_cap_cr": 20_000,
        "market_regime_score": 80, "circuit_utilization_pct": 0.1,
        "days_to_major_event": 10, "promoter_pledge_pct": 0.01,
        "regulatory_risk_score": 0.1, "adversarial_risk": 0.1,
        "distribution_risk": 0.1, "ephemeral_news_risk": 0.1,
        "data_quality": 0.98, "out_of_distribution": 0.1,
        "gap_pct": 0.02, "rvol_20d": 3.0, "sector_strength_score": 90,
        "technical_score": 90, "volume_score": 95, "institutional_score": 85,
        "catalyst_score": 80, "mtf_alignment": 0.9,
    }


def test_bad_liquidity_is_rejected() -> None:
    features = good_features()
    features["turnover_cr"] = 10
    candidate = evaluate("TEST", datetime.now(timezone.utc), features)
    prediction = score_candidate(candidate)
    assert prediction.decision == Decision.NO_TRADE


def test_pipeline_is_not_allowed_to_invent_probability() -> None:
    candidate = evaluate("TEST", datetime.now(timezone.utc), good_features())
    prediction = score_candidate(candidate)
    assert prediction.probability_target_before_stop == 0.0
