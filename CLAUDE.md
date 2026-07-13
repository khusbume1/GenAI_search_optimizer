# GEO Search Optimizer project guidance

## Purpose
This application wraps the installed `/geo` Claude Code skill with repeatable execution, persistence, comparison, and reporting.

## Architecture
- `geo_optimizer/runner.py`: validates URLs, invokes Claude Code, locates reports, and records results.
- `geo_optimizer/parser.py`: extracts scores and summaries from generated Markdown.
- `geo_optimizer/storage.py`: SQLite persistence.
- `api.py`: FastAPI interface.
- `dashboard.py`: Streamlit dashboard.
- `.claude/skills/geo-growth-plan/`: turns an audit into an implementation backlog.

## Non-negotiable rules
- Respect robots.txt and the upstream skill's crawl/rate limits.
- Never change or deploy anything to the audited website.
- Do not claim guaranteed placement in ChatGPT, Claude, Perplexity, Gemini, or Google AI Overviews.
- Keep execution scoped to the per-audit run directory.
- Add parser tests whenever report formats change.

## Common commands
- `geo-search doctor`
- `geo-search audit https://example.com --mode full`
- `geo-search compare https://site-a.com https://site-b.com`
- `streamlit run dashboard.py`
- `uvicorn api:app --reload`
- `pytest`
