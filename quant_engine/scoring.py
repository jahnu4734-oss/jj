from __future__ import annotations

from .models import Candidate, Decision, Prediction


def score_candidate(candidate: Candidate) -> Prediction:
    """Apply safety gates before a future calibrated ML model.

    This intentionally does not claim predictive accuracy. Thresholds and
    probabilities must be learned from point-in-time out-of-sample tests.
    """
    if candidate.hard_failures:
        return Prediction(
            symbol=candidate.symbol,
            probability_target_before_stop=0.0,
            expected_return=0.0,
            expected_loss=0.0,
            risk_reward=0.0,
            model_disagreement=1.0,
            data_quality=0.0,
            out_of_distribution=1.0,
            decision=Decision.NO_TRADE,
            reasons=candidate.hard_failures,
        )

    # Placeholder until trained models are introduced.
    return Prediction(
        symbol=candidate.symbol,
        probability_target_before_stop=0.0,
        expected_return=0.0,
        expected_loss=0.0,
        risk_reward=0.0,
        model_disagreement=1.0,
        data_quality=0.0,
        out_of_distribution=1.0,
        decision=Decision.NO_TRADE,
        reasons=["No calibrated model is installed yet."],
    )
