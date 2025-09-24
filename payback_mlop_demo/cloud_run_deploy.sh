#!/usr/bin/env bash
# Example deploy script to Google Cloud Run.
# Requires gcloud CLI, authenticated user and enabled APIs.
# Edit PROJECT_ID, REGION and IMAGE variables before running.

PROJECT_ID="your-gcp-project-id"
REGION="europe-west3"
IMAGE="gcr.io/${PROJECT_ID}/payback-mlops-demo:latest"

# Build & push (local docker build + gcloud auth configure-docker)
# docker build -t ${IMAGE} .
# docker push ${IMAGE}

# Deploy to Cloud Run (uncomment when ready)
# gcloud run deploy payback-mlops-demo --image ${IMAGE} --region ${REGION} --platform managed --allow-unauthenticated
