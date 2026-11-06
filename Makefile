.PHONY: setup baseline analyze figures

setup:
	uv sync --locked

baseline:
	uv run squares baseline --output outputs/baselines/grid.csv

analyze:
	uv run python scripts/analysis/analyze_baseline.py

figures:
	uv run --with matplotlib python scripts/analysis/plot_baseline_analysis.py
