from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

default_args = {"start_date": datetime(2025, 5, 15)}

with DAG(
    "extract_entsoe_data",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["entsoe"]
) as dag:
    extract = BashOperator(
        task_id="run_entsoe_fetcher",
        bash_command="python /opt/airflow/src/extract/universal_entsoe_data_featcher.py"
    )

    trigger_forecast = TriggerDagRunOperator(
        task_id="trigger_transform_forecast",
        trigger_dag_id="transform_forecast_data"
    )

    trigger_generation = TriggerDagRunOperator(
        task_id="trigger_transform_generation",
        trigger_dag_id="transform_generation_data"
    )

    extract >> [trigger_forecast, trigger_generation]