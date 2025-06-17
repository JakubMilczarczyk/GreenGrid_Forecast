from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

default_args = {"start_date": datetime(2025, 5, 15)}

with DAG(
    "extract_weather_data",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["weather"]
) as dag:
    extract = BashOperator(
        task_id="run_weather_fetcher",
        bash_command="python /opt/airflow/src/extract/featch_weather_data.py"
    )

    trigger_data_merger = TriggerDagRunOperator(
        task_id="trigger_train_features_data_merger",
        trigger_dag_id="train_features_data_merger"
    )

    extract >> trigger_data_merger