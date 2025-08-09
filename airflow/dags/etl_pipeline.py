from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"start_date": datetime(2025, 5, 15)}

with DAG(
    "etl_pipeline",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["ETL"],
    description="ETL pipeline: Extracts data from ENTSO-E and weather API then processes it and saves.",
) as dag:
    featch_entsoe_data = BashOperator(
        task_id="run_entsoe_fetcher",
        bash_command="python /opt/airflow/src/extract/universal_entsoe_data_featcher.py"
    )

    extract_wether_data = BashOperator(
        task_id="run_weather_fetcher",
        bash_command="python /opt/airflow/src/extract/featch_weather_data.py"
    )

    transform_entsoe_forecast_data = BashOperator(
        task_id="run_entsoe_forecast_transformer",
        bash_command="python /opt/airflow/src/transform/entsoe_forecast_parser.py"
    )

    transform_entsoe_generation_data = BashOperator(
        task_id="run_entsoe_generation_transformer",
        bash_command="python /opt/airflow/src/transform/entsoe_generation_parser.py"
    )

    merge_faetures_data = BashOperator(
        task_id="merge_features_data",
        bash_command="python /opt/airflow/src/transform/train_features_data_merger.py"
    )

    [featch_entsoe_data, extract_wether_data] >> transform_entsoe_forecast_data
    transform_entsoe_forecast_data >> transform_entsoe_generation_data
    transform_entsoe_generation_data >> merge_faetures_data
