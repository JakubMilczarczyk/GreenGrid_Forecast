import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from utils.forecast.forecast import run_forecast

default_args = {"start_date": datetime(2025, 5, 15)}

def check_model():
    if not os.path.exists('/opt/services/airflow/shared/models/saved_models/linear_regression_model.joblib'): # TODO: change to the input model path (input from UI or API)
        raise FileNotFoundError("Model file not found. Please ensure the model is available at the specified path.")

def check_data():
    if not os.path.exists('/opt/services/airflow/shared/data/splits/x_test.parquet'): # TODO: change to the actual input file path
        raise FileNotFoundError("Input data file not found. Please ensure the data is available at the specified path.")

with DAG(
    'forecast_pipeline',
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=['Forecast'],
    description='Forecast pipeline: Check data, model avalibility and runs the forecasting model and saves the predictions.',
) as dag:
    check_data_task = PythonOperator(
        task_id='check_data',
        python_callable=check_data
    )

    check_model_task = PythonOperator(
        task_id='check_model',
        python_callable=check_model
    )

    run_forecast_task = PythonOperator(
        task_id='run_forecast',
        python_callable=run_forecast
    )

    check_data_task >> check_model_task >> run_forecast_task
