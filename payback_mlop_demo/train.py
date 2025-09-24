import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

DATA_PATH = "data/sample_data.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    X = df.drop(columns=['target'])
    y = df['target']
    return X, y

def create_synthetic_data(path=DATA_PATH, n=1000, random_state=42):
    np.random.seed(random_state)
    dates = pd.date_range('2020-01-01', periods=n, freq='D')
    trend = np.linspace(0, 10, n)
    seasonal = 5 * np.sin(np.linspace(0, 20, n))
    noise = np.random.normal(0, 1, n)
    value = trend + seasonal + noise
    df = pd.DataFrame({
        'ds': dates,
        'lag_1': np.roll(value, 1),
        'lag_7': np.roll(value, 7),
        'rolling_mean_7': pd.Series(value).rolling(7, min_periods=1).mean(),
        'exog': np.random.normal(0,1,n),
        'target': value
    })
    df.fillna(method='bfill', inplace=True)
    df.to_csv(path, index=False)
    print(f"Synthetic sample data written to {path}")

def train_and_save():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    joblib.dump({'model': model}, MODEL_PATH)
    print(f"Model trained and saved to {MODEL_PATH} — MSE: {mse:.4f}")

if __name__ == '__main__':
    if not os.path.exists('data') or not os.path.exists(DATA_PATH):
        os.makedirs('data', exist_ok=True)
        create_synthetic_data(DATA_PATH, n=200)
    train_and_save()
