from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"start_date": datetime(2025, 5, 15)}

with DAG(
    "train_model_pipeline",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["Train"],
    description="Train model pipeline: prepares features data and trains the model.",
) as dag:
    prepare_data_to_train = BashOperator(
        task_id="prepare_data_to_train",
        bash_command="python /opt/airflow/src/utils/prepare_data_to_train.py"
    )

    train_model = BashOperator(
        task_id="train_and_save_model",
        bash_command="python /opt/airflow/src/utils/train_model.py"
    )

    [prepare_data_to_train] >> train_model
