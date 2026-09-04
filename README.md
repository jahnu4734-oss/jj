# India Quant Decision Engine

A research-grade framework for an Indian-equity prediction system designed to **rank at most two opportunities or return NO TRADE**.

## V1 now includes

- 36-layer rule registry derived from the strategy specification
- 500+ feature budget across market, sector, price, volume, volatility, F&O, institutional, fundamentals, valuation, events, news, microstructure, historical analogues, and model-health families
- Point-in-time observation contracts and future-information checks
- Deterministic hard filters and vetoes
- Conservative OHLC backtest resolution when stop and target occur in the same bar
- Auditable candidate/prediction models
- Research CLI
- Tests for look-ahead protection, trade resolution, feature coverage, and hard-filter behavior

## Research guardrails

The code does **not** invent a win probability before a calibrated model is trained. A high score is not a performance claim. Thresholds in the 36 layers are hypotheses and must be validated with walk-forward, out-of-sample testing.

The system must be allowed to return **NO TRADE**. Never force a daily pick merely to satisfy a product requirement.

## Architecture

`data -> point-in-time validation -> feature engineering -> 36-layer filters -> specialist models -> ensemble -> historical analogues -> adversarial analysis -> uncertainty/OOD checks -> risk engine -> ranking -> 0/1/2 decisions`

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
python -m quant_engine.cli status
python -m quant_engine.cli features
python -m quant_engine.cli demo DEMO
```

The data adapter layer is intentionally provider-neutral. Add licensed NSE/vendor/broker adapters only after the research schema is stable.

**Live order execution is disabled.** Move through historical validation, walk-forward testing, paper trading, and only then consider controlled execution with the applicable Indian regulatory and broker requirements.
