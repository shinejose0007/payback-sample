# Airflow DAG placeholder - copy into an Airflow instance and adjust commands
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mlops_demo',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('retrain_pipeline', start_date=datetime(2025,1,1), schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    extract = BashOperator(task_id='extract_data', bash_command='python scripts/extract_features.py || true')
    train = BashOperator(task_id='train_model', bash_command='python train.py')
    notify = BashOperator(task_id='notify', bash_command='echo "Retrain finished"')
    extract >> train >> notify
