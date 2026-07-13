# Generative AI Search Optimizer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A portfolio-ready **Generative Engine Optimization (GEO)** platform that turns Claude Code GEO skills into a repeatable application with a CLI, REST API, dashboard, structured report parsing, SQLite history, competitor comparison, and implementation planning.

<img width="819" height="410" alt="image" src="https://github.com/user-attachments/assets/93512f0b-88b5-42d8-948d-e9d29a51338c" />



## Why I built this project

Traditional SEO tools mainly evaluate web search signals. Generative search experiences also need content that is easy for AI systems to discover, understand, attribute, and cite. This project demonstrates how an existing Claude skill can be transformed into a small software product with validation, orchestration, persistence, APIs, visualization, testing, and documentation.

The application integrates with the open-source [`geo-seo-claude`](https://github.com/zubair-trabzada/geo-seo-claude) project as an external dependency. The upstream skill performs specialized GEO analysis; this repository supplies the product and engineering layer around it.

## Project at a glance

| Area | Implementation |
|---|---|
| User interfaces | Streamlit dashboard, CLI, FastAPI REST API |
| AI orchestration | Claude Code CLI invoking `/geo` skills |
| Inputs | Public URL, audit mode, optional comparison URLs |
| Processing | Validation, isolated run creation, Claude execution, report discovery, parsing, persistence |
| Outputs | GEO score, category scores, findings, Markdown report, JSON result, audit history |
| Data store | SQLite for local development |
| Reliability | Timeout handling, exit-code checks, parser tests, environment diagnostics |
| Demonstration | Local demo mode that requires no Claude account or live website crawl |

## Input → Process → Output

<p align="center">
  <img width="386" height="398" alt="image" src="https://github.com/user-attachments/assets/6c978d04-88e7-45af-a735-943a3c1baac8" />
</p>



<p align="center"><em>Figure 1 — A website URL is validated, analyzed through either the live Claude path or local demo path, structured, persisted, and delivered as actionable GEO results.</em></p>

### Input

A user provides:

- A public HTTP or HTTPS website URL
- An audit mode such as `full`, `citability`, `schema`, or `technical`
- Optionally, multiple URLs for a comparison
- Optionally, demo mode for a fully local walkthrough

Example:

```json
{
  "url": "https://example.com",
  "mode": "full"
}
```

### Process

1. The URL is normalized and checked to reject localhost, credentials, private IPs, and unsupported schemes.
2. A unique audit ID and isolated directory are created under `data/runs/`.
3. The application writes `audit-request.json` so the original input is reproducible.
4. For a live audit, the runner invokes Claude Code with the corresponding `/geo` command.
5. Claude and the installed GEO skill inspect relevant GEO dimensions and generate a report.
6. The application locates the generated report and extracts:
   - Overall GEO score
   - Rating
   - Category scores
   - Executive summary
   - Findings grouped by severity
7. Structured results are stored in SQLite and written to `audit-result.json`.
8. The dashboard, API, and CLI expose the same persisted result.

### Output

Each run can produce:

```text
data/runs/<timestamp>-<domain>-<audit-id>/
├── audit-request.json       # normalized input and execution metadata
├── claude-output.txt        # raw Claude output for live audits
├── GEO-AUDIT-REPORT.md      # generated or demo audit report
└── audit-result.json        # structured application output
```

Example structured output:

```json
{
  "overall_score": 72,
  "rating": "Fair",
  "categories": {
    "AI Citability": 64,
    "Technical GEO": 86
  },
  "severity_counts": {
    "critical": 1,
    "high": 2,
    "medium": 2,
    "low": 1
  }
}
```

## Architecture

<p align="center">
  <img width="236" height="370" alt="image" src="https://github.com/user-attachments/assets/372d64ba-1f40-4a0b-b192-83ee59bd0547" />
</p>

<p align="center"><em>Figure 2 — Layered architecture separating presentation, orchestration, AI execution, deterministic structuring, and persistence.</em></p>

## Features

- **Multiple audit modes:** full, quick, citability, crawler access, `llms.txt`, brand signals, platform readiness, schema, technical, content, and client report
- **Demo mode:** creates a complete audit result without Claude Code or network access
- **Audit history:** persists results in SQLite for later review
- **Competitor comparison:** runs and ranks multiple domains
- **Structured parsing:** converts Markdown reports into scores and actionable findings
- **REST API:** exposes audit, history, comparison, and demo endpoints
- **Interactive dashboard:** visualizes scorecards, findings, reports, and run metadata
- **Claude project skill:** converts audit reports into a 90-day implementation backlog
- **Traceability:** saves both the normalized request and structured result for each run
- **CI pipeline:** runs linting and automated tests on GitHub Actions

## Repository structure

```text
geo-search-optimizer/
├── .claude/skills/geo-growth-plan/  # project-specific Claude skill
├── .github/workflows/ci.yml         # automated lint and test workflow
├── docs/                            # technical docs and editable diagrams
├── examples/                        # sample input and output files
├── geo_optimizer/
│   ├── cli.py                       # command-line interface
│   ├── config.py                    # environment configuration
│   ├── models.py                    # application data models
│   ├── parser.py                    # GEO report parser
│   ├── runner.py                    # Claude orchestration and demo execution
│   ├── service.py                   # shared initialized services
│   └── storage.py                   # SQLite persistence
├── tests/                           # unit and API tests
├── api.py                           # FastAPI application
├── dashboard.py                     # Streamlit application
├── pyproject.toml                   # package and dependencies
└── scripts/bootstrap.sh             # full setup including upstream skill
```

## Open and run in Visual Studio Code on Windows

The downloadable ZIP is the complete runnable product. After extracting it:

1. Open **Visual Studio Code**.
2. Select **File → Open Folder** and choose `generative-ai-search-optimizer`.
3. Double-click `setup_windows.bat` once to create the Python environment and install dependencies.
4. Double-click `run_dashboard.bat` to start the product.
5. Open `http://localhost:8501` if the browser does not open automatically.
6. Keep **Demo mode** enabled and click **Run audit**. Demo mode works without Claude Code or a Claude account.

You can also use VS Code tasks through **Terminal → Run Task**:

- `Setup project`
- `Run dashboard`
- `Run API`
- `Run tests`

The main runnable files are:

- `dashboard.py` — Streamlit product interface
- `api.py` — FastAPI service
- `geo_optimizer/runner.py` — audit orchestration
- `geo_optimizer/parser.py` — Markdown-to-JSON report parsing
- `geo_optimizer/storage.py` — SQLite persistence

## Quick start: demo mode

Demo mode is the easiest way for a recruiter or reviewer to run the project. It does not require Claude Code and does not fetch a website.

```bash
# 1. Clone your repository
git clone https://github.com/OWNER/REPOSITORY.git
cd REPOSITORY

# 2. Create the environment and install the app
python3 -m venv .venv
source .venv/bin/activate          # Windows Git Bash: source .venv/Scripts/activate
python -m pip install -e '.[dev]'

# 3. Run a complete local demo
geo-search demo --url https://example.com

# 4. Launch the dashboard
streamlit run dashboard.py
```

In the dashboard, keep **Demo mode** enabled and select **Run audit**.

## Live audit setup with Claude Code

Live audits require:

- Python 3.10+
- Git
- Claude Code CLI installed and authenticated
- Internet access

Review the script and run:

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
geo-search doctor
```

The bootstrap script clones the upstream GEO skill into `vendor/` and runs its local installer. This repository does not vendor or redistribute the upstream source code.

Run a live audit:

```bash
geo-search audit https://example.com --mode full
```

## CLI examples

```bash
# Environment check
geo-search doctor

# Local demonstration
geo-search demo --url https://example.com

# Live audits
geo-search audit https://example.com --mode full
geo-search audit https://example.com/article --mode citability
geo-search audit https://example.com --mode schema

# Compare sites
geo-search compare https://example.com https://competitor.com --mode full

# Demo comparison
geo-search compare https://example.com https://competitor.example --demo

# Stored history
geo-search history --domain example.com
geo-search show <audit-id>

# Parse an existing report
geo-search parse-report examples/output/SAMPLE-GEO-AUDIT-REPORT.md
```

## REST API

Start the server:

```bash
uvicorn api:app --reload
```

Interactive OpenAPI documentation:

```text
http://127.0.0.1:8000/docs
```

Run the local demo endpoint:

```bash
curl -X POST http://127.0.0.1:8000/demo/audits \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com"}'
```

Run a live audit:

```bash
curl -X POST http://127.0.0.1:8000/audits \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","mode":"full"}'
```

See [`docs/05-API-REFERENCE.md`](docs/05-API-REFERENCE.md) for the complete contract.

## Streamlit dashboard

```bash
streamlit run dashboard.py
```

The dashboard provides:

- New audit form
- Demo/live execution switch
- Audit history table
- Overall score and rating
- Category score chart
- Actionable finding table
- Full report preview and download
- Execution metadata for traceability

## Project-specific Claude skill

After a live or demo report exists, open Claude Code in the project and run:

```text
/geo-growth-plan data/runs/<run-folder>/GEO-AUDIT-REPORT.md
```

The skill generates `GEO-IMPLEMENTATION-PLAN.md` with:

- 0–7 day immediate fixes
- 8–30 day foundation work
- 31–90 day authority and content work
- Owner roles, effort, acceptance criteria, and measurement metrics

## Testing

```bash
pytest -q
ruff check .
```

The tests cover:

- URL normalization and safety validation
- Prompt construction
- Score and rating extraction
- Category parsing
- Finding extraction by severity
- Demo audit persistence
- API health and demo endpoints

GitHub Actions runs the same checks for every push and pull request.

## Engineering decisions

- **SQLite** keeps the portfolio version simple and reproducible.
- **Per-run directories** preserve traceability and prevent report collisions.
- **One shared service layer** keeps CLI, dashboard, and API behavior consistent.
- **Demo mode** removes external credentials as a barrier to evaluation.
- **Markdown parsing** separates AI-generated narrative from application data.
- **External integration** keeps upstream ownership and licensing clear.

Read the design rationale in [`docs/08-DESIGN-DECISIONS.md`](docs/08-DESIGN-DECISIONS.md).

## Limitations

- Live audit quality depends on the installed upstream skill and accessible website content.
- The Markdown parser supports common report structures but may require updates if upstream headings change.
- SQLite and synchronous API execution are intended for a local portfolio project, not multi-tenant production use.
- GEO scores are diagnostic indicators; they do not guarantee citation, ranking, traffic, or conversion outcomes.
- The project does not modify or deploy changes to the audited website.

## Production roadmap

1. Move audit execution to a queue worker.
2. Replace SQLite with Postgres and store reports in object storage.
3. Add authentication, organizations, role-based access, and quotas.
4. Add scheduled re-audits and score-delta notifications.
5. Add a documented prompt/query evaluation set for AI visibility testing.
6. Add CMS integrations that create drafts with human approval.
7. Add observability, retry policies, audit logs, and cost controls.

## Attribution

This application integrates with [`zubair-trabzada/geo-seo-claude`](https://github.com/zubair-trabzada/geo-seo-claude), an MIT-licensed project. Its authors own and maintain the upstream skill. This repository contains an independent application layer and installs the upstream project as an external dependency.

## License

This application layer is available under the [MIT License](LICENSE). See [NOTICE](NOTICE) for upstream attribution.
