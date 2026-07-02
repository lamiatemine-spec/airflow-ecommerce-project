from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract_data():
    print("Extraction des données en cours...")

with DAG('ecommerce_extraction', start_date=datetime(2026, 1, 1), schedule_interval='@daily', catchup=False) as dag:
    task_extract = PythonOperator(task_id='extract_task', python_callable=extract_data)