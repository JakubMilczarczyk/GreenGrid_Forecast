from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

default_args = {"start_date": datetime(2025, 5, 15)}

with DAG(
    "merge_train_features_data",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["train"]
) as dag:
    merge = BashOperator(
        task_id="merge_features_data",
        bash_command="python /opt/airflow/src/transform/train_features_data_merger.py"
    )

    trigger_train = TriggerDagRunOperator(
        task_id="trigger_train_model",
        trigger_dag_id="train_model"
    )

    merge >> trigger_train