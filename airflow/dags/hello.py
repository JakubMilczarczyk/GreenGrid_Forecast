from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG(
    dag_id='hello_world',
    start_date=datetime.now(),
    schedule_interval='@daily',
    catchup=False,
    tags=['example'],
) as dag:
    start = DummyOperator(task_id='start')

def print_hello():
    print(f"Hello World! It's {datetime.now()}. Kuba ;]")

print_task = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
)

start >> print_task
