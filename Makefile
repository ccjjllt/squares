.PHONY: setup baseline

setup:
	uv sync --locked

baseline:
	uv run --no-sync squares baseline --output outputs/baselines/grid.csv
