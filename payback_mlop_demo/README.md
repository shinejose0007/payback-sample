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

---
Viel Erfolg bei der Bewerbung — passe das PoC bei Bedarf an (z.B. Vertex AI, BigQuery, Terraform-Module).
