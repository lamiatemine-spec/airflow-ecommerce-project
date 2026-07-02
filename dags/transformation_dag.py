from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def transform_data():
    print("Transformation des données en cours...")

with DAG('ecommerce_transformation', start_date=datetime(2026, 1, 1), schedule_interval='@daily', catchup=False) as dag:
    task_transform = PythonOperator(task_id='transform_task', python_callable=transform_data)