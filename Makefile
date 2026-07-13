.PHONY: setup install doctor test lint demo dashboard api audit clean

setup:
	./scripts/bootstrap.sh

install:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -e '.[dev]'

doctor:
	.venv/bin/geo-search doctor

test:
	.venv/bin/pytest -q

lint:
	.venv/bin/ruff check .

demo:
	.venv/bin/geo-search demo --url https://example.com

dashboard:
	.venv/bin/streamlit run dashboard.py

api:
	.venv/bin/uvicorn api:app --reload

audit:
	@test -n "$(URL)" || (echo "Usage: make audit URL=https://example.com" && exit 1)
	.venv/bin/geo-search audit "$(URL)" --mode full

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ geo_optimizer/__pycache__ tests/__pycache__
