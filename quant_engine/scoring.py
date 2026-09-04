from __future__ import annotations

from math import isfinite
from .models import Candidate, Decision, Prediction


def _num(candidate: Candidate, key: str, default: float | None = None) -> float | None:
    value = candidate.feature_values.get(key, default)
    if value is None:
        return default
    try:
        value_f = float(value)
    except (TypeError, ValueError):
        return default
    return value_f if isfinite(value_f) else default


def score_candidate(candidate: Candidate) -> Prediction:
    reasons: list[str] = []
    if candidate.hard_failures or candidate.vetoes:
        reasons.extend(candidate.hard_failures)
        reasons.extend(candidate.vetoes)
        return Prediction(
            symbol=candidate.symbol, as_of=candidate.as_of,
            probability_target_before_stop=0.0, expected_return=0.0,
            expected_loss=0.0, risk_reward=0.0, model_disagreement=1.0,
            data_quality=candidate.data_quality, out_of_distribution=candidate.out_of_distribution,
            decision=Decision.NO_TRADE, final_score=0.0, reasons=reasons,
        )

    rr = _num(candidate, "risk_reward", 0.0) or 0.0
    regime = _num(candidate, "market_regime_score", 0.0) or 0.0
    sector = _num(candidate, "sector_strength_score", 0.0) or 0.0
    technical = _num(candidate, "technical_score", 0.0) or 0.0
    volume = _num(candidate, "volume_score", 0.0) or 0.0
    institutional = _num(candidate, "institutional_score", 0.0) or 0.0
    catalyst = _num(candidate, "catalyst_score", 0.0) or 0.0
    mtf = _num(candidate, "mtf_alignment", 0.0) or 0.0
    # This score is a research baseline only; probabilities are intentionally not inferred.
    raw = (
        0.15 * regime + 0.12 * sector + 0.14 * technical + 0.14 * volume
        + 0.10 * institutional + 0.10 * catalyst + 0.10 * mtf
        + 0.10 * min(rr / 2.0, 1.0) + 0.05 * candidate.data_quality
    ) * 100.0
    final_score = max(0.0, min(100.0, raw))

    if rr < 2.0:
        reasons.append("Risk/reward is below the research minimum of 1:2.")
    if candidate.out_of_distribution > 0.70:
        reasons.append("Candidate is outside the model's supported distribution.")
    if candidate.data_quality < 0.90:
        reasons.append("Data quality is below the live-research threshold.")

    decision = Decision.WATCH
    if not reasons and candidate.confirmed_rules >= 28 and final_score >= 85:
        decision = Decision.BUY
        reasons.append("Passes the initial deterministic research gates; ML calibration still required.")
    elif reasons:
        decision = Decision.NO_TRADE

    return Prediction(
        symbol=candidate.symbol, as_of=candidate.as_of,
        probability_target_before_stop=0.0, expected_return=0.0,
        expected_loss=0.0, risk_reward=rr,
        model_disagreement=1.0, data_quality=candidate.data_quality,
        out_of_distribution=candidate.out_of_distribution,
        decision=decision, final_score=final_score, reasons=reasons,
    )
