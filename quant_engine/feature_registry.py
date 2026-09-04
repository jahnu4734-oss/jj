from __future__ import annotations

from dataclasses import dataclass
from .features import FEATURES, FAMILIES, feature_count, feature_keys


@dataclass(frozen=True)
class FeatureMetadata:
    key: str
    family: str
    target_horizon: str
    leakage_sensitive: bool = True


FEATURE_METADATA = tuple(
    FeatureMetadata(f.key, f.family, "1-5d", f.point_in_time_required)
    for f in FEATURES
)

# Additional derived/context features reserved for later research. They are
# intentionally named separately so adding them does not accidentally create
# hidden leakage in a backtest.
DERIVED_FEATURES = tuple(
    f"{base}_{window}d_{transform}"
    for base in (
        "ret", "volume_ratio", "delivery_pct", "rsi", "atr_pct",
        "relative_strength", "oi_change", "iv", "margin", "eps_growth",
    )
    for window in (1, 3, 5, 10, 20, 50, 100)
    for transform in ("level", "zscore", "rank", "slope")
)


def total_feature_budget() -> int:
    return feature_count() + len(DERIVED_FEATURES)


def registry_report() -> dict[str, int]:
    return {
        "base_features": feature_count(),
        "derived_features": len(DERIVED_FEATURES),
        "total_budget": total_feature_budget(),
        "families": len(FAMILIES),
    }


__all__ = ["FEATURE_METADATA", "DERIVED_FEATURES", "FEATURES", "feature_keys", "registry_report"]
