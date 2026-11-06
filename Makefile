.PHONY: setup check test baseline smoke

setup:
	uv sync --locked

check:
	uv run ruff check .
	uv run ruff format --check src tests

test:
	uv run pytest

baseline:
	uv run squares baseline --output outputs/grid.csv

smoke:
	uv run squares baseline --max-n 10 --output outputs/smoke.csv
	uv run squares score outputs/smoke.csv --max-n 10 --workers 2 --output-dir outputs/smoke-report
