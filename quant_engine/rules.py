from dataclasses import dataclass
from enum import Enum


class RuleKind(str, Enum):
    HARD = "hard"
    SCORE = "score"
    VETO = "veto"
    META = "meta"


@dataclass(frozen=True)
class RuleSpec:
    id: int
    name: str
    description: str
    kind: RuleKind
    feature_keys: tuple[str, ...]
    threshold: float | None = None


RULES: tuple[RuleSpec, ...] = (
    RuleSpec(1, "universe", "Nifty 200; average daily volume > 500000 shares", RuleKind.HARD, ("universe_nifty200", "avg_volume_20d"), 500000),
    RuleSpec(2, "gap_scanner", "Premarket gap magnitude > 1.5% hypothesis", RuleKind.SCORE, ("gap_pct",), 0.015),
    RuleSpec(3, "volume_anomaly", "09:15-09:30 volume versus comparable 10-day baseline", RuleKind.SCORE, ("opening_15m_rvol",), 1.35),
    RuleSpec(4, "delivery_spike", "Delivery percentage above rolling baseline", RuleKind.SCORE, ("delivery_z20",), 1.0),
    RuleSpec(5, "key_level", "Price near validated 52-week extreme or support/resistance", RuleKind.SCORE, ("distance_52w_extreme", "distance_key_level"), 0.005),
    RuleSpec(6, "catalyst", "News/results/orders/block deals inside point-in-time window", RuleKind.SCORE, ("catalyst_score",), 0.5),
    RuleSpec(7, "options_oi", "ATM OI/PCR context", RuleKind.SCORE, ("atm_oi_z", "pcr_z"), 0.0),
    RuleSpec(8, "sector_alignment", "Sector momentum aligned with direction", RuleKind.SCORE, ("sector_rs_20d",), 0.0),
    RuleSpec(9, "relative_strength", "Stock strength versus Nifty and sector", RuleKind.SCORE, ("rs_nifty_20d", "rs_sector_20d"), 0.0),
    RuleSpec(10, "technical_pattern", "Flag/base/breakout structure", RuleKind.SCORE, ("breakout_score", "base_quality"), 0.5),
    RuleSpec(11, "depth_imbalance", "Opening bid/ask depth imbalance", RuleKind.SCORE, ("depth_imbalance",), 0.0),
    RuleSpec(12, "previous_close_behavior", "Previous-day final 30-minute behaviour", RuleKind.SCORE, ("late_day_momentum",), 0.0),
    RuleSpec(13, "ownership", "Institutional-grade float/promoter profile", RuleKind.HARD, ("promoter_holding_pct", "free_float_pct"), 0.45),
    RuleSpec(14, "institutional_activity", "FII/DII stock/sector activity", RuleKind.SCORE, ("institutional_flow_z",), 0.0),
    RuleSpec(15, "circuit_proximity", "Reject excessive price-band usage", RuleKind.VETO, ("circuit_utilization_pct",), 0.80),
    RuleSpec(16, "smart_money", "Block/bulk/insider activity", RuleKind.SCORE, ("smart_money_score",), 0.0),
    RuleSpec(17, "structure_quality", "Contraction followed by expansion", RuleKind.SCORE, ("range_contraction", "breakout_volume_ratio"), 0.0),
    RuleSpec(18, "risk_reward", "Minimum 1:2 candidate R:R hypothesis", RuleKind.HARD, ("risk_reward",), 2.0),
    RuleSpec(19, "liquidity_quality", "Turnover and spread constraints", RuleKind.HARD, ("turnover_cr", "spread_pct"), 50.0),
    RuleSpec(20, "event_calendar", "Reject imminent high-impact events", RuleKind.VETO, ("days_to_major_event",), 3.0),
    RuleSpec(21, "rvol", "Relative volume > 2.5 hypothesis", RuleKind.SCORE, ("rvol_20d",), 2.5),
    RuleSpec(22, "gap_hold", "Gap remains materially unfilled after opening window", RuleKind.SCORE, ("gap_fill_ratio_15m",), 0.50),
    RuleSpec(23, "sector_duplication", "Avoid redundant sector exposure", RuleKind.VETO, ("sector_candidate_count",), 3.0),
    RuleSpec(24, "promoter_quality", "Pledge and regulatory checks", RuleKind.VETO, ("promoter_pledge_pct", "regulatory_risk_score"), 0.10),
    RuleSpec(25, "adversarial_ai", "Structured failure-case analysis", RuleKind.VETO, ("adversarial_risk",), 0.70),
    RuleSpec(26, "multi_timeframe", "Daily/weekly/15m alignment", RuleKind.SCORE, ("mtf_alignment",), 0.67),
    RuleSpec(27, "three_day_accumulation", "Three-day delivery accumulation", RuleKind.SCORE, ("delivery_trend_3d",), 0.0),
    RuleSpec(28, "high_breakout", "52-week breakout with exceptional volume", RuleKind.SCORE, ("is_52w_breakout", "breakout_volume_ratio"), 3.0),
    RuleSpec(29, "base_length", "Minimum base duration hypothesis", RuleKind.SCORE, ("base_days",), 120.0),
    RuleSpec(30, "market_cap", "Market cap > 5000 crore hypothesis", RuleKind.HARD, ("market_cap_cr",), 5000.0),
    RuleSpec(31, "earnings_growth", "Two consecutive quarters of growth", RuleKind.SCORE, ("earnings_growth_score",), 0.5),
    RuleSpec(32, "distribution_check", "Reject distribution signatures", RuleKind.VETO, ("distribution_risk",), 0.60),
    RuleSpec(33, "sector_rank", "Sector in top 3 weekly performers", RuleKind.SCORE, ("sector_rank",), 3.0),
    RuleSpec(34, "nifty_regime", "Nifty weekly trend/distribution check", RuleKind.HARD, ("market_regime_score",), 0.0),
    RuleSpec(35, "convergence", "Initial convergence hypothesis", RuleKind.META, ("confirmed_rule_count",), 28.0),
    RuleSpec(36, "news_spike", "Short-lived corporate-news spike handling", RuleKind.VETO, ("ephemeral_news_risk",), 0.70),
)
