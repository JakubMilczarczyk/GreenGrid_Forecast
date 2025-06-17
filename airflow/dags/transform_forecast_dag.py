from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

default_args = {"start_date": datetime(2025, 5, 15)}

with DAG(
    "transform_forecast_data",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["transform"]
) as dag:
    transform = BashOperator(
        task_id="parse_forecast_xml",
        bash_command="python /opt/airflow/src/transform/entsoe_forecast_parser.py"
    )

    trigger_extract_weather = TriggerDagRunOperator(
        task_id="trigger_extract_weather_data",
        trigger_dag_id="extract_weather_data"
    )

    transform >> trigger_extract_weather