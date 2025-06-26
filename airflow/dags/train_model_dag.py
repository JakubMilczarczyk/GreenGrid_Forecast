from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pathlib import Path
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
default_args = {'start_date': datetime(2025, 5, 15)}

def train_model_if_needed():
    MODEL_PATH = Path('opt/airflow/models/saved_models/linear_regression_model.joblib')
    if MODEL_PATH.exists():
        logging.info(f'Model already exists. Skipping training')
        return
    subprocess.run(['python', '/opt/airflow/src/utils/trainer.py'], check=True)

with DAG(
    'train_model',
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=['train']
) as dag:
    train = PythonOperator(
        task_id='train_model_if_needed',
        python_callable=train_model_if_needed
    )