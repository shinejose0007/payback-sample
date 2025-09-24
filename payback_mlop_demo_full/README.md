# PAYBACK MLOps Demo - Enhanced

This enhanced demo includes additional MLOps features useful for job applications:

- Fixed training to drop non-numeric `ds` column.
- Model manifest written to `models/manifest.json`.
- Optional artifact upload to local `artifacts/` or Google Cloud Storage via `MODEL_GCS_BUCKET`.
- Feature store (SQLite) via `feature_store.py` and `scripts/extract_features.py`.
- Serving improvements: `/health`, `/ready`, input validation, prediction logging to `logs/predictions.jsonl`.
- Scripts: `scripts/explain.py` (permutation importance), `scripts/aggregate_metrics.py`.
- CI template with commented deploy steps for GitHub Actions and Jenkinsfile example.
- Airflow DAG placeholder and Terraform templates.

## Quickstart
1. Create venv and install:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Train model:
   ```bash
   python train.py
   ```
3. Run server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
4. Predict:
   ```bash
   curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"features": [12.3, 11.0, 10.8, 0.12]}'
   ```

## Notes
- For GCS upload/download set `MODEL_GCS_BUCKET` and authenticate with Google Cloud SDK/service account.
- This is a PoC. For production, implement secure secrets handling, robust monitoring, and proper CI/CD with secrets.
