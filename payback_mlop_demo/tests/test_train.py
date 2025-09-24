import os
import joblib
from train import create_synthetic_data, train_and_save

def test_training_creates_model(tmp_path):
    # prepare data
    data_dir = tmp_path / 'data'
    data_dir.mkdir()
    data_file = data_dir / 'sample_data.csv'
    create_synthetic_data(str(data_file), n=200)
    # copy to default path for train.py to find
    os.makedirs('data', exist_ok=True)
    os.replace(str(data_file), 'data/sample_data.csv')
    # run train
    train_and_save()
    assert os.path.exists('models/model.pkl')
    model_obj = joblib.load('models/model.pkl')
    assert 'model' in model_obj
