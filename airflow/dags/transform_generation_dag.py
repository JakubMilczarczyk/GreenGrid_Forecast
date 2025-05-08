from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"start_date": datetime(2025, 5, 1)}

with DAG("transform_generation_data", schedule_interval="@daily", catchup=False, default_args=default_args, tags=["transform"]) as dag:
    transform = BashOperator(
        task_id="parse_generation_xml",
        bash_command="python /opt/airflow/src/transform/entsoe_generation_parser.py"
    )
