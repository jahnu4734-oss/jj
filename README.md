# India Quant Decision Engine

Research-grade framework for building, testing, and operating a multi-layer Indian equity decision engine.

## Core principles

- No guaranteed predictions or win-rate promises.
- Point-in-time data only for backtests.
- No look-ahead bias, survivorship bias, or leakage tolerated.
- Hard vetoes can reject a trade regardless of model score.
- The model may return **NO TRADE**.
- Backtest -> walk-forward -> paper trading -> controlled live deployment.
- Every prediction and every input is audit logged.

## Initial architecture

1. Data contracts and point-in-time timestamps
2. Universe and liquidity filters
3. Market regime engine
4. Sector ranking
5. 36-layer rule engine
6. Feature registry for 500+ features
7. ML probability models
8. Historical analogue engine
9. News/adversarial analysis
10. Risk and portfolio constraints
11. Calibration and model-health monitoring
12. Morning ranking and reporting

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
python -m quant_engine.cli --help
```

Do not connect real broker execution until the research and paper-trading gates pass.
