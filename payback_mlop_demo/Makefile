.PHONY: train test build run

train:
	python train.py

test:
	pytest -q

build:
	docker build -t payback-mlops-demo:latest .

run:
	uvicorn app.main:app --reload --port 8000
