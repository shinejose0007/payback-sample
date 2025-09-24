import joblib, numpy as np, os
from sklearn.inspection import permutation_importance
import pandas as pd

MODEL_PATH = os.environ.get('MODEL_PATH', 'models/model.pkl')
DATA_PATH = os.environ.get('DATA_PATH', 'data/sample_data.csv')

def compute_permutation_importance():
    model = joblib.load(MODEL_PATH)['model']
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=['target','ds'])
    y = df['target']
    r = permutation_importance(model, X, y, n_repeats=5, random_state=0)
    imp = {c: float(v) for c,v in zip(X.columns, r.importances_mean)}
    print('Permutation importances:', imp)
    return imp

if __name__ == '__main__':
    if not os.path.exists(MODEL_PATH):
        print('Model not found. Run train.py first.')
    else:
        compute_permutation_importance()
