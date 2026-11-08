.PHONY: setup baseline

setup:
	uv sync --locked --extra experiments

baseline:
	uv run squares baseline --output outputs/baselines/grid.csv
