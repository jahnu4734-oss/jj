from quant_engine.feature_registry import registry_report


def test_feature_budget_exceeds_500() -> None:
    report = registry_report()
    assert report["base_features"] > 200
    assert report["total_budget"] >= 500
