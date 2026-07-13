FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY geo_optimizer ./geo_optimizer
COPY examples ./examples
COPY api.py dashboard.py ./
RUN pip install --no-cache-dir .

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
