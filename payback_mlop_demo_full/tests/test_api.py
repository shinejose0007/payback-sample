from fastapi.testclient import TestClient
import os
from app.main import app
from train import create_synthetic_data, train_and_save

client = TestClient(app)

def setup_module(module):
    if not os.path.exists('data/sample_data.csv'):
        os.makedirs('data', exist_ok=True)
        create_synthetic_data('data/sample_data.csv', n=200)
    train_and_save()

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'

def test_ready():
    r = client.get('/ready')
    assert r.status_code == 200
    assert r.json().get('ready') == True

def test_predict():
    import pandas as pd
    df = pd.read_csv('data/sample_data.csv')
    row = df.iloc[10]
    features = [float(row['lag_1']), float(row['lag_7']), float(row['rolling_mean_7']), float(row['exog'])]
    r = client.post('/predict', json={'features': features})
    assert r.status_code == 200
    assert 'prediction' in r.json()
