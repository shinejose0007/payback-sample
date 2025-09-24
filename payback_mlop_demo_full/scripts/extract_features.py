import pandas as pd
from feature_store import write_features
import os
DATA_PATH = os.environ.get('DATA_PATH', 'data/sample_data.csv')

def run():
    if not os.path.exists(DATA_PATH):
        print('Data not found. Run create_synthetic_data or train.py to create data.')
        return
    df = pd.read_csv(DATA_PATH)
    write_features(df.head(50))
    print('Wrote recent features to feature store.')

if __name__ == '__main__':
    run()
