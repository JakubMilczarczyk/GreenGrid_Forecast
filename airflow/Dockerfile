FROM apache/airfow:2.8.1-python3.11

USER root
COPY requirements.txt .
RUN pip install --no-cache-dir -r /requirements.txt

USER airflow
COPY dags/ /opt/airflow/dags/
COPY airflow.cfg /opt/airflow/airflow.cfg