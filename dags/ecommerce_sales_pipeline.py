from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime

# Fonction de traitement des données
def process_data():
    print("Traitement des données lancé...")

# Arguments par défaut du DAG
default_args = {
    'owner': 'airflow', 
    'start_date': datetime(2026, 6, 1)
}

# Définition du DAG
with DAG(
    'ecommerce_sales_pipeline', 
    default_args=default_args, 
    schedule_interval=None,
    catchup=False
) as dag:

    # FileSensor configuré pour surveiller le fichier dataset.csv
    # Le timeout limite le temps d'attente avant l'échec de la tâche
    wait_for_file = FileSensor(
        task_id='wait_for_file', 
        filepath='/opt/airflow/data/dataset.csv', 
        fs_conn_id='fs_default',
        poke_interval=10,
        timeout=300  # Arrête la recherche après 300 secondes (5 minutes)
    )
    
    # Opérateur pour traiter les données après la détection du fichier
    task_process = PythonOperator(
        task_id='process_data', 
        python_callable=process_data
    )
    
    # Définition de la dépendance
    wait_for_file >> task_process