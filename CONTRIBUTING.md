# Contributing

1. Create a feature branch.
2. Keep AI orchestration separate from deterministic parsing and persistence.
3. Add or update tests for behavior changes.
4. Run `pytest -q` and `ruff check .`.
5. Document any report-format assumptions.
6. Do not commit credentials, generated audit data, or the cloned `vendor/` directory.
7. Preserve upstream attribution.
