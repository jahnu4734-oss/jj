from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from .models import Candidate
from .rules import RULES, RuleKind


@dataclass(frozen=True)
class PipelineConfig:
    min_confirmed_rules: int = 28
    min_data_quality: float = 0.90
    max_ood_score: float = 0.70


def _f(features: dict[str, float | None], key: str, default: float = 0.0) -> float:
    value = features.get(key)
    return default if value is None else float(value)


def evaluate(symbol: str, as_of: datetime, features: dict[str, float | None], config: PipelineConfig | None = None) -> Candidate:
    cfg = config or PipelineConfig()
    hard_failures: list[str] = []
    vetoes: list[str] = []
    evidence: dict[str, float] = {}
    confirmed = 0

    checks = {
        "universe": _f(features, "universe_nifty200", 0.0) >= 1,
        "avg_volume": _f(features, "avg_volume_20d", 0.0) >= 500_000,
        "ownership": _f(features, "promoter_holding_pct", 0.0) >= 0.45,
        "risk_reward": _f(features, "risk_reward", 0.0) >= 2.0,
        "liquidity_turnover": _f(features, "turnover_cr", 0.0) > 50.0,
        "spread": _f(features, "spread_pct", 1.0) < 0.002,
        "market_cap": _f(features, "market_cap_cr", 0.0) > 5000.0,
        "market_regime": _f(features, "market_regime_score", -1.0) >= 0.0,
        "circuit": _f(features, "circuit_utilization_pct", 0.0) <= 0.80,
        "event": _f(features, "days_to_major_event", 999.0) >= 3.0,
        "promoter_pledge": _f(features, "promoter_pledge_pct", 0.0) < 0.10,
        "regulatory": _f(features, "regulatory_risk_score", 0.0) < 0.70,
    }

    for name, passed in checks.items():
        evidence[name] = 1.0 if passed else 0.0
        if not passed:
            hard_failures.append(name)
        else:
            confirmed += 1

    veto_checks = {
        "adversarial_risk": _f(features, "adversarial_risk", 0.0) > cfg.max_ood_score,
        "distribution_risk": _f(features, "distribution_risk", 0.0) > 0.60,
        "ephemeral_news": _f(features, "ephemeral_news_risk", 0.0) > 0.70,
        "data_quality": _f(features, "data_quality", 0.0) < cfg.min_data_quality,
        "ood": _f(features, "out_of_distribution", 1.0) > cfg.max_ood_score,
    }
    for name, failed in veto_checks.items():
        evidence[name] = 0.0 if failed else 1.0
        if failed:
            vetoes.append(name)
        else:
            confirmed += 1

    for key in ("gap_pct", "rvol_20d", "sector_strength_score", "technical_score", "volume_score", "institutional_score", "catalyst_score", "mtf_alignment"):
        evidence[key] = _f(features, key)
        if evidence[key] > 0:
            confirmed += 1

    return Candidate(
        symbol=symbol,
        as_of=as_of,
        feature_values=features,
        hard_failures=hard_failures,
        vetoes=vetoes,
        evidence=evidence,
        confirmed_rules=min(36, confirmed),
        data_quality=max(0.0, min(1.0, _f(features, "data_quality", 0.0))),
        out_of_distribution=max(0.0, min(1.0, _f(features, "out_of_distribution", 1.0))),
    )
