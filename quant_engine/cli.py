from __future__ import annotations

import argparse
from datetime import datetime, timezone

from .feature_registry import registry_report
from .pipeline import evaluate
from .scoring import score_candidate


def main() -> None:
    parser = argparse.ArgumentParser(description="India Quant Decision Engine")
    parser.add_argument("--version", action="version", version="0.1.0")
    sub = parser.add_subparsers(dest="command", required=False)
    sub.add_parser("status")
    sub.add_parser("features")
    demo = sub.add_parser("demo")
    demo.add_argument("symbol", nargs="?", default="DEMO")
    args = parser.parse_args()

    if args.command in (None, "status"):
        print("India Quant Decision Engine: research core ready")
        print("Live trading: DISABLED")
        print(f"Feature budget: {registry_report()['total_budget']}")
        return
    if args.command == "features":
        print(registry_report())
        return
    if args.command == "demo":
        now = datetime.now(timezone.utc)
        features = {
            "universe_nifty200": 1, "avg_volume_20d": 1_000_000,
            "promoter_holding_pct": 0.52, "risk_reward": 2.4,
            "turnover_cr": 120.0, "spread_pct": 0.001, "market_cap_cr": 25000.0,
            "market_regime_score": 82, "circuit_utilization_pct": 0.10,
            "days_to_major_event": 8, "promoter_pledge_pct": 0.01,
            "regulatory_risk_score": 0.05, "adversarial_risk": 0.15,
            "distribution_risk": 0.10, "ephemeral_news_risk": 0.10,
            "data_quality": 0.98, "out_of_distribution": 0.08,
            "gap_pct": 0.021, "rvol_20d": 3.1, "sector_strength_score": 91,
            "technical_score": 94, "volume_score": 96, "institutional_score": 85,
            "catalyst_score": 88, "mtf_alignment": 0.90,
        }
        candidate = evaluate(args.symbol, now, features)
        print(score_candidate(candidate).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
