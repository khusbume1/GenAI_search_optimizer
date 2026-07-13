from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from geo_optimizer.runner import SUPPORTED_MODES
from geo_optimizer.service import runner, store

app = FastAPI(
    title="Generative AI Search Optimizer API",
    version="1.0.0",
    description=(
        "Portfolio API for running Claude Code GEO audits, parsing reports, "
        "tracking history, and comparing websites."
    ),
)


class AuditRequest(BaseModel):
    url: str = Field(min_length=4, examples=["https://example.com"])
    mode: str = Field(default="full")


class DemoAuditRequest(BaseModel):
    url: str = Field(default="https://example.com", min_length=4)


class CompareRequest(BaseModel):
    urls: list[str] = Field(min_length=2, max_length=10)
    mode: str = Field(default="full")
    demo: bool = Field(default=False)


@app.get("/health", tags=["System"])
def health() -> dict:
    issues = runner.check_environment()
    return {
        "status": "ready" if not issues else "demo-only",
        "live_audit_issues": issues,
        "demo_mode_available": True,
    }


@app.post("/audits", tags=["Audits"])
def create_audit(request: AuditRequest) -> dict:
    if request.mode not in SUPPORTED_MODES:
        raise HTTPException(400, f"Unsupported mode: {request.mode}")
    result = runner.run(request.url, request.mode)
    if result.status == "failed":
        raise HTTPException(500, result.as_dict())
    return result.as_dict()


@app.post("/demo/audits", tags=["Demo"])
def create_demo_audit(request: DemoAuditRequest) -> dict:
    result = runner.run_demo(request.url)
    if result.status == "failed":
        raise HTTPException(500, result.as_dict())
    return result.as_dict()


@app.post("/comparisons", tags=["Audits"])
def create_comparison(request: CompareRequest) -> dict:
    if request.mode not in SUPPORTED_MODES:
        raise HTTPException(400, f"Unsupported mode: {request.mode}")
    results = [
        (runner.run_demo(url) if request.demo else runner.run(url, request.mode)).as_dict()
        for url in request.urls
    ]
    results.sort(
        key=lambda item: item["overall_score"] if item["overall_score"] is not None else -1,
        reverse=True,
    )
    return {"mode": request.mode, "demo": request.demo, "results": results}


@app.get("/audits", tags=["History"])
def list_audits(
    limit: int = Query(default=50, ge=1, le=500), domain: str | None = None
) -> list[dict]:
    return store.list(limit=limit, domain=domain)


@app.get("/audits/{audit_id}", tags=["History"])
def get_audit(audit_id: str) -> dict:
    item = store.get(audit_id)
    if not item:
        raise HTTPException(404, "Audit not found")
    return item
