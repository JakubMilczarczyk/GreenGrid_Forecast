from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

defult_args = {'start_date': datetime(2025, 5, 15)}

with DAG(
    'train_model',
    schedule_interval=None,
    catchup=False,
    default_args=defult_args,
    tags=['train']
) as dag:
    train = BashOperator(
        task_id='run_trainer',
        bash_command='python /opt/airflow/src/utils/trainer.py'
    )