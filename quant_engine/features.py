from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureSpec:
    key: str
    family: str
    description: str
    availability: str
    point_in_time_required: bool = True


FAMILIES: dict[str, list[str]] = {
    "market": ["nifty_1d_ret", "nifty_5d_ret", "nifty_20d_ret", "nifty_above_20dma", "nifty_above_50dma", "nifty_above_200dma", "nifty_rsi", "india_vix", "india_vix_percentile", "advance_decline", "pct_nifty_above_20dma", "pct_nifty_above_50dma", "new_high_low_ratio", "fii_market_flow", "global_risk_score"],
    "sector": ["sector_1d_ret", "sector_5d_ret", "sector_20d_ret", "sector_rs_20d", "sector_rsi", "sector_adx", "sector_volume_ratio", "sector_breadth", "sector_above_50dma", "sector_rank", "sector_institutional_flow", "sector_volatility", "sector_momentum_percentile", "sector_rotation_score", "sector_regime"],
    "price": ["ret_1d", "ret_3d", "ret_5d", "ret_10d", "ret_20d", "ret_50d", "ret_100d", "ret_200d", "price_vs_20dma", "price_vs_50dma", "price_vs_200dma", "distance_52w_high", "distance_52w_low", "breakout_5d", "breakout_10d", "breakout_20d", "breakout_50d", "swing_high_breakout", "market_structure_score", "candle_body_strength", "upper_wick_ratio", "lower_wick_ratio", "opening_range_score", "vwap_distance", "vwap_slope"],
    "volume": ["volume_ratio_5d", "volume_ratio_10d", "volume_ratio_20d", "volume_ratio_50d", "rvol_20d", "opening_15m_rvol", "volume_acceleration", "breakout_volume_ratio", "up_down_volume_ratio", "delivery_pct", "delivery_z20", "delivery_trend_3d", "delivery_price_divergence", "obv_slope", "mfi", "accumulation_distribution", "volume_contraction", "volume_expansion", "turnover_cr", "turnover_percentile"],
    "volatility": ["atr14", "atr_pct", "atr_percentile", "hist_vol_20d", "volatility_expansion", "volatility_contraction", "bollinger_width", "bollinger_percent_b", "bollinger_squeeze", "keltner_squeeze", "intraday_range_pct", "gap_volatility", "sector_relative_volatility"],
    "fno": ["futures_basis", "futures_oi_change", "futures_price_change", "long_buildup_score", "short_buildup_score", "short_covering_score", "long_unwinding_score", "atm_call_oi", "atm_put_oi", "atm_call_oi_change", "atm_put_oi_change", "pcr", "pcr_change", "pcr_z", "atm_iv", "iv_percentile", "iv_change", "call_put_iv_skew", "max_pain_distance", "options_volume_ratio"],
    "institutional": ["fii_holding_pct", "fii_holding_change", "dii_holding_pct", "dii_holding_change", "mf_holding_change", "insurance_holding_change", "institutional_buy_days", "institutional_sell_days", "block_deal_direction", "block_deal_premium", "bulk_deal_direction", "insider_buying", "insider_selling", "insider_cluster_score", "institutional_flow_z"],
    "fundamental": ["revenue_growth_yoy", "revenue_growth_qoq", "ebitda_growth", "ebit_growth", "pat_growth", "eps_growth", "eps_acceleration", "ebitda_margin", "margin_change", "roe", "roce", "free_cash_flow", "fcf_growth", "debt_equity", "interest_coverage", "cash_flow_quality", "working_capital_trend", "earnings_surprise", "revenue_surprise", "guidance_revision"],
    "valuation": ["pe", "forward_pe", "pb", "ev_ebitda", "peg", "ev_sales", "fcf_yield", "pe_percentile", "sector_relative_valuation", "valuation_growth_gap"],
    "events": ["days_to_earnings", "days_to_agm", "days_to_exdiv", "days_to_bonus", "days_to_split", "buyback_event", "fundraising_event", "qip_event", "rights_issue_event", "promoter_transaction", "pledge_change", "rating_change", "regulatory_risk_score", "litigation_risk_score", "major_event_score"],
    "news": ["news_sentiment", "sentiment_momentum", "catalyst_score", "catalyst_novelty", "news_credibility", "source_count", "positive_negative_ratio", "management_tone", "earnings_call_sentiment", "guidance_sentiment", "analyst_sentiment", "regulatory_news_risk", "competitive_risk", "industry_news_alignment", "news_price_reaction", "news_volume_reaction", "unexpected_news_score", "narrative_momentum", "contradictory_news_score", "ephemeral_news_risk"],
    "microstructure": ["spread_pct", "bid_depth", "ask_depth", "depth_imbalance", "order_flow_imbalance", "opening_auction_imbalance", "trade_size_skew", "quote_update_rate", "market_impact_estimate", "liquidity_stress"],
    "historical": ["similar_setup_count", "historical_win_rate", "historical_median_return", "historical_median_drawdown", "historical_profit_factor", "historical_avg_time_target", "historical_avg_time_stop", "bull_regime_win_rate", "bear_regime_win_rate", "high_vix_win_rate", "low_vix_win_rate", "earnings_window_win_rate", "sector_regime_win_rate", "setup_similarity", "historical_sample_quality"],
    "model": ["model_probability_1", "model_probability_2", "model_probability_3", "ensemble_probability", "probability_calibration", "model_disagreement", "feature_concentration", "out_of_distribution", "regime_similarity", "prediction_stability", "prediction_change", "model_uncertainty", "data_quality", "adversarial_risk", "final_expected_value"],
}

FEATURES: tuple[FeatureSpec, ...] = tuple(
    FeatureSpec(key, family, f"{family} feature: {key}", "point-in-time")
    for family, keys in FAMILIES.items()
    for key in keys
)


def feature_keys() -> tuple[str, ...]:
    return tuple(feature.key for feature in FEATURES)


def feature_count() -> int:
    return len(FEATURES)
