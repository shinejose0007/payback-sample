from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

MODEL_PATH = os.path.join('models','model.pkl')

app = FastAPI(title="PAYBACK MLOps Demo - Model Serving")

class PredictRequest(BaseModel):
    features: list

@app.on_event('startup')
def load_model():
    global _model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model artifact not found at {MODEL_PATH}. Run train.py first.")
    payload = joblib.load(MODEL_PATH)
    _model = payload['model']

@app.post('/predict')
def predict(req: PredictRequest):
    try:
        arr = np.array(req.features).reshape(1, -1)
        pred = _model.predict(arr)[0]
        return {'prediction': float(pred)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/health')
def health():
    return {'status': 'ok'}
