from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"start_date": datetime(2025, 5, 1)}

with DAG("run_streamlit_app", schedule_interval=None, catchup=False, default_args=default_args, tags=["dashboard"]) as dag:
    dashboard = BashOperator(
        task_id="launch_streamlit",
        bash_command="streamlit run /opt/airflow/app/streamlitt_app.py"
    )
