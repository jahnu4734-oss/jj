"""Initial rule specification.

These are deliberately represented as named rules rather than baked-in model
weights. Thresholds are hypotheses to be validated by point-in-time research.
"""

RULES = {
    1: ("universe", "Nifty 200; average daily volume > 500000 shares"),
    2: ("gap_scanner", "premarket gap > 1.5% from previous close"),
    3: ("volume_anomaly", "09:15-09:30 volume > 35% of 10-day comparable average"),
    4: ("delivery_spike", "delivery percentage materially above 10-day baseline"),
    5: ("key_level", "within 0.5% of 52-week extreme or validated S/R"),
    6: ("catalyst", "news/results/orders/block deals within 48h"),
    7: ("options_oi", "ATM OI buildup and PCR context"),
    8: ("sector_alignment", "sector momentum aligned with trade direction"),
    9: ("relative_strength", "strength versus Nifty and sector"),
    10: ("technical_pattern", "flag/base/breakout on 10-day structure"),
    11: ("depth_imbalance", "opening bid/ask depth imbalance"),
    12: ("previous_close_behavior", "previous-day final 30-minute behaviour"),
    13: ("ownership", "institutional-grade float/promoter profile"),
    14: ("institutional_activity", "FII/DII stock/sector activity"),
    15: ("circuit_proximity", "reject excessive price-band usage"),
    16: ("smart_money", "block/bulk/insider activity"),
    17: ("structure_quality", "contraction followed by expansion"),
    18: ("risk_reward", "minimum candidate R:R 1:2 hypothesis"),
    19: ("liquidity_quality", "turnover/spread constraints"),
    20: ("event_calendar", "reject imminent high-impact events"),
    21: ("rvol", "relative volume > 2.5 hypothesis"),
    22: ("gap_hold", "gap remains materially unfilled after 15m"),
    23: ("sector_duplication", "avoid redundant sector exposure"),
    24: ("promoter_quality", "pledge/investigation checks"),
    25: ("adversarial_ai", "structured failure-case analysis"),
    26: ("multi_timeframe", "daily/weekly/15m alignment"),
    27: ("three_day_accumulation", "delivery accumulation for 3 days"),
    28: ("high_breakout", "52-week breakout with exceptional volume"),
    29: ("base_length", "minimum base duration hypothesis"),
    30: ("market_cap", "market cap > 5000 crore hypothesis"),
    31: ("earnings_growth", "two consecutive quarters of growth"),
    32: ("distribution_check", "reject distribution signatures"),
    33: ("sector_rank", "sector in top 3 weekly performers"),
    34: ("nifty_regime", "Nifty weekly trend and distribution check"),
    35: ("convergence", "minimum 28/36 initial confirmation hypothesis"),
    36: ("news_spike", "short-lived corporate-news spike handling"),
}
