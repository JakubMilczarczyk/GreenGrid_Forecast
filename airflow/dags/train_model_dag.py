from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pathlib import Path
import subprocess
import logging
import sys

default_args = {'start_date': datetime(2025, 5, 15)}

def train_model_if_needed():
    MODEL_PATH = Path('/opt/airflow/models/saved_models/linear_regression_model.joblib')
    PYTHON_EXECUTABLE = "/usr/local/bin/python"
    if MODEL_PATH.exists():
        logging.info('Model already exists. Skipping training.')
        return
    try:
        subprocess.run([PYTHON_EXECUTABLE, '/opt/airflow/src/utils/prepare_data_to_train.py'], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f'Preparing train data failed with error: {e}')
        raise
    try:
        subprocess.run([sys.executable, '/opt/airflow/src/utils/train_model.py'], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f'Training model failed with error: {e}')
        raise

with DAG(
    'train_model',
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=['train'],
) as dag:
    train = PythonOperator(
        task_id='train_model_if_needed',
        python_callable=train_model_if_needed
    )