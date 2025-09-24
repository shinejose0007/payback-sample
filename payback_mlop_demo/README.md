# PAYBACK MLOps Demo (Minimal)
Kurz: Dieses Repository ist ein kleines, lokal ausführbares MLOps-Demoprojekt, passend als PoC für Bewerbungen im Bereich MLOps/Data Engineering.

---

## Inhalt
- `train.py` – Trainings-Skript: erstellt ein einfaches Regressionsmodell (scikit-learn) auf synthetischen Zeitreihenfeatures und speichert `models/model.pkl`.
- `app/main.py` – FastAPI-App: lädt `models/model.pkl` und bietet einen `/predict` Endpoint.
- `Dockerfile` – containerisiert die FastAPI-App.
- `requirements.txt` – benötigte Python-Pakete.
- `terraform/main.tf` – Platzhalter und Beispiel für GCP (BigQuery / Cloud Storage / Cloud Run). **Nur als Vorlage**.
- `.github/workflows/ci.yml` – Beispiel CI: installiert deps, führt Tests aus und baut ein Docker-Image.
- `Jenkinsfile` – Beispiel-Pipeline (Declarative).
- `cloud_run_deploy.sh` – Beispielskript für `gcloud`-Deployment (erfordert gcloud)
- `tests/test_train.py` – einfacher Unit-Test für das Trainingsscript.
- `Makefile` – Komfortziele zum Train, Test, Build.

## Quickstart (lokal)
1. Python 3.9+ venv anlegen und aktivieren.
2. `pip install -r requirements.txt`
3. `python train.py`  # trainiert Modell und schreibt models/model.pkl
4. `uvicorn app.main:app --reload --port 8000`
5. POST `http://localhost:8000/predict` mit JSON `{"features": [1.2, 0.3, ...]}`

## Hinweise
- Dieses Repo ist ein **PoC**: es zeigt End-to-End-Komponenten (Training, Containerisierung, Serving, CI/CD-Vorlage, Terraform-Beispiel). Produktionseinsatz erfordert Anpassungen, sichere Secrets-Handling, GCP-Authentifizierung und echte Infrastruktur.
- Terraform-Dateien sind Beispiele und nicht automatisch ausgeführt.






# wider cutting (More Explanation)

Make sure you have installed on your machine:

Python 3.9 or 3.10

virtualenv or venv (or use conda)

pip

(optional, for container/local testing) Docker

(optional, for cloud deploy) Google Cloud SDK (gcloud) and a GCP project + permissions

If you downloaded the ZIP from the environment, unzip it and cd into the project root:

unzip payback_mlop_demo.zip
cd payback_mlop_demo

1) Quick local run (recommended first)

Create and activate a virtual environment, install deps, train the model, run the API:

python -m venv .venv
source .venv/bin/activate    # Linux / macOS
# .venv\Scripts\activate     # Windows PowerShell

pip install -r requirements.txt


Train the model (this creates models/model.pkl):

python train.py


Start the FastAPI server (serving expects the model file to exist):

uvicorn app.main:app --reload --port 8000


Open health endpoint to verify:

GET http://localhost:8000/health
# returns {"status":"ok"}

2) Example predict request

Important: the training uses these numeric input columns (features): lag_1, lag_7, rolling_mean_7, exog — that is 4 numeric features. The predict endpoint expects a JSON body with "features": [<4 numbers>].

Example curl:

curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features":[12.3, 11.0, 10.8, 0.12]}'


Response:

{"prediction": 13.12345}

3) Run tests

The repo includes a small pytest test:

pytest -q


(note: running tests will call train.py, so ensure you have permissions to create data/ and models/).

4) Run with Docker (locally)

Build the image and run the container:

docker build -t payback-mlops-demo:latest .
docker run --rm -p 8000:8000 payback-mlops-demo:latest


Then call the /predict endpoint as above.

5) Deploy to Cloud Run (high-level)

cloud_run_deploy.sh is a template. Typical steps (you must configure and authenticate gcloud first):

Build and push image to a registry (GCR or Artifact Registry):

docker build -t gcr.io/YOUR_PROJECT_ID/payback-mlops-demo:latest .
docker push gcr.io/YOUR_PROJECT_ID/payback-mlops-demo:latest


Deploy to Cloud Run:

gcloud run deploy payback-mlops-demo \
  --image gcr.io/YOUR_PROJECT_ID/payback-mlops-demo:latest \
  --region europe-west3 \
  --platform managed --allow-unauthenticated


Note: you must set up service account permissions, enable APIs, and adapt the app to read model artifact from Cloud Storage (recommended) rather than local models/.

6) CI/CD examples

.github/workflows/ci.yml demonstrates installing deps, running tests and building Docker image (local runner must have Docker).

Jenkinsfile shows a simple pipeline (checkout → install → test → build).
Use these as templates; in production you’d add steps to push images to a registry, run integration tests, and deploy to Cloud Run/Vertex AI.

7) Important fix / required improvement (must do before training)

One small bug to address before you rely on this demo: the training currently keeps the ds (date string) column in features. scikit-learn models require numeric features — training will fail or behave incorrectly if ds remains a string. You should remove ds from X or convert it to numeric features (e.g., day-of-week, ordinal).

Quick fix: edit train.py -> change the load_data function to drop 'ds':

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    # drop non-numeric columns like ds (date string)
    X = df.drop(columns=['target', 'ds'])
    y = df['target']
    return X, y


After that, re-run python train.py and training will run using the numeric features (lag_1, lag_7, rolling_mean_7, exog).

8) Where to improve this PoC to better match the job requirements

If you plan to show this as part of an MLOps job application, consider adding:

GCP integration:

Upload trained artifact to Cloud Storage and load it from there in the app.

Store features or logs in BigQuery.

Use Vertex AI for managed model deployment (or show a Vertex AI deployment example).

Earth that actually provisions the Cloud Run service, bucket and BigQuery dataset (with variables and state backend).

CI/CD deployment: GitHub Actions job to build image, push to registry, and run gcloud run deploy (with secrets stored in Actions).

Monitoring & observability:

Add basic metrics (response times, request counts) and model-performance logging.

Add an example drift detection or alert (push key metrics to Stackdriver/Cloud Monitoring).

Model versioning & reproducibility:

Integrate MLflow or DVC for model + data versioning; produce reproducible training runs.

Security / secrets:

Use secret manager for GCP credentials, don't store secrets in code.

9) Troubleshooting tips

If uvicorn fails on startup: ensure models/model.pkl exists (run python train.py first).

If Docker build fails: check network or pip dependency issues; try pip install -r requirements.txt locally first.

If pytest fails: look at stack trace — most likely missing model file or file permissions. Delete models/ and re-run python train.py to recreate artifact.

10) Quick checklist to prepare this PoC for sending with an application

Fix ds column as shown above and re-run training.

Add a short README section that explains expected feature order for /predict.

Commit a small GitHub repo and link it in your CV/cover letter (that helps a lot).

Add a short script that uploads the model to a Cloud Storage bucket (so you can claim Cloud storage usage).

Optionally add a short demo notebook or screenshots of the API call and a returned prediction.
