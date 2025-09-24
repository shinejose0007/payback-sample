from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist
import joblib
import numpy as np
import os, json, time, logging

MODEL_PATH = os.environ.get('MODEL_PATH', os.path.join('models','model.pkl'))
GCS_BUCKET = os.environ.get('MODEL_GCS_BUCKET', None)
PRED_LOG = os.environ.get('PRED_LOG', 'logs/predictions.jsonl')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('mlops-demo')

app = FastAPI(title="PAYBACK MLOps Demo - Model Serving")

class PredictRequest(BaseModel):
    features: conlist(float, min_items=4, max_items=4)

@app.on_event('startup')
def load_model():
    global _model
    if GCS_BUCKET:
        try:
            from google.cloud import storage
            client = storage.Client()
            bucket = client.bucket(GCS_BUCKET)
            blob_name = os.environ.get('MODEL_GCS_PREFIX','') + os.path.basename(MODEL_PATH)
            blob = bucket.blob(blob_name)
            if blob.exists():
                os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
                blob.download_to_filename(MODEL_PATH)
                logger.info(f"Downloaded model from gs://{GCS_BUCKET}/{blob_name}")
        except Exception as e:
            logger.warning(f"Could not download model from GCS: {e}")
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model artifact not found at {MODEL_PATH}. Run train.py first.")
    payload = joblib.load(MODEL_PATH)
    _model = payload['model']
    logger.info("Model loaded")

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/ready')
def ready():
    return {'ready': os.path.exists(MODEL_PATH)}

@app.post('/predict')
def predict(req: PredictRequest):
    try:
        arr = np.array(req.features).reshape(1, -1)
        pred = _model.predict(arr)[0]
        response = {'prediction': float(pred)}
        os.makedirs(os.path.dirname(PRED_LOG), exist_ok=True)
        entry = {
            'ts': time.time(),
            'features': req.features,
            'prediction': float(pred)
        }
        with open(PRED_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
        logger.info(f"Prediction made: {response}")
        return response
    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=400, detail=str(e))
