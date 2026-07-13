from __future__ import annotations

from pathlib import Path

import streamlit as st

from geo_optimizer.runner import SUPPORTED_MODES
from geo_optimizer.service import runner, store

st.set_page_config(page_title="Generative AI Search Optimizer", page_icon="🔎", layout="wide")
st.title("Generative AI Search Optimizer")
st.caption(
    "Portfolio application for GEO audits, AI-search readiness, competitor benchmarking, and progress tracking."
)

issues = runner.check_environment()
if issues:
    st.info(
        "Live Claude audits are not configured, but the bundled demo works immediately.\n\n"
        + "\n".join(f"- {issue}" for issue in issues)
    )

with st.sidebar:
    st.header("New audit")
    url = st.text_input("Website URL", value="https://example.com")
    use_demo = st.toggle("Demo mode", value=bool(issues), help="Uses bundled sample data; no Claude CLI required.")
    mode = st.selectbox(
        "Audit mode", options=list(SUPPORTED_MODES), index=0, disabled=use_demo
    )
    run_clicked = st.button("Run audit", type="primary", use_container_width=True)
    st.divider()
    st.markdown(
        "**Input:** public website URL  \n"
        "**Process:** Claude GEO skill → parser → SQLite  \n"
        "**Output:** score, findings, report, history"
    )

if run_clicked:
    if not url.strip():
        st.error("Enter a website URL.")
    else:
        with st.spinner("Processing the audit..."):
            result = runner.run_demo(url) if use_demo else runner.run(url, mode)
        if result.status == "failed":
            st.error(result.error or "Audit failed")
            if result.stdout:
                with st.expander("Execution output"):
                    st.code(result.stdout)
        else:
            st.success(f"Audit completed: {result.audit_id}")
            st.session_state["selected_audit_id"] = result.audit_id

history = store.list(limit=100)
if not history:
    st.info("No audits yet. Run the bundled demo from the sidebar.")
    st.stop()

st.subheader("Audit history")
rows = [
    {
        "Audit": item["id"],
        "Domain": item["domain"],
        "Mode": item["mode"],
        "Execution": item.get("execution_type", "live"),
        "Status": item["status"],
        "Score": item["overall_score"],
        "Rating": item["rating"],
        "Started": item["started_at"],
    }
    for item in history
]
st.dataframe(rows, use_container_width=True, hide_index=True)

ids = [item["id"] for item in history]
default_id = st.session_state.get("selected_audit_id", ids[0])
default_index = ids.index(default_id) if default_id in ids else 0
selected_id = st.selectbox("Open audit", ids, index=default_index)
audit = store.get(selected_id)
if not audit:
    st.stop()

score_col, rating_col, status_col, issues_col = st.columns(4)
score_col.metric("GEO score", audit["overall_score"] if audit["overall_score"] is not None else "—")
rating_col.metric("Rating", audit["rating"] or "—")
status_col.metric("Status", audit["status"].title())
issues_col.metric("Priority findings", sum(audit["severity_counts"].values()))

if audit["summary"]:
    st.subheader("Executive summary")
    st.write(audit["summary"])

if audit["categories"]:
    st.subheader("Category scores")
    st.bar_chart(audit["categories"], horizontal=True)

if audit["findings"]:
    st.subheader("Actionable findings")
    st.dataframe(audit["findings"], use_container_width=True, hide_index=True)
elif audit["severity_counts"]:
    st.subheader("Finding severity")
    st.bar_chart(audit["severity_counts"])

report_path = audit.get("report_path")
if report_path and Path(report_path).exists():
    path = Path(report_path)
    st.subheader("Generated report")
    if path.suffix.lower() in {".md", ".txt"}:
        report_text = path.read_text(encoding="utf-8", errors="replace")
        with st.expander("Preview report", expanded=False):
            st.markdown(report_text)
        st.download_button(
            "Download report",
            data=report_text,
            file_name=path.name,
            mime="text/markdown" if path.suffix.lower() == ".md" else "text/plain",
        )
    else:
        st.write(path)

with st.expander("Execution details"):
    st.json(
        {
            "audit_id": audit["id"],
            "url": audit["url"],
            "mode": audit["mode"],
            "execution_type": audit.get("execution_type"),
            "run_dir": audit["run_dir"],
            "report_path": audit.get("report_path"),
        }
    )
    st.code(audit.get("stdout") or "No execution output stored.")
