from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"start_date": datetime(2025, 5, 1)}

with DAG("extract_entsoe_data", schedule_interval="@daily", catchup=False, default_args=default_args, tags=["entsoe"]) as dag:
    extract = BashOperator(
        task_id="run_entsoe_fetcher",
        bash_command="python /opt/airflow/src/extract/universal_entsoe_data_featcher.py"
    )
