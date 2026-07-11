from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
from pymongo import MongoClient  # Import direct de pymongo
import pandas as pd
import os
import logging

# Configuration des chemins dans le conteneur
DATA_PATH = "/opt/airflow/data/dataset.csv"
ERROR_PATH = "/opt/airflow/data/errors.csv"

def validate_and_process(**kwargs):
    """
    Traitement robuste : Nettoyage, calculs et isolation des erreurs.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Le fichier attendu est introuvable à : {DATA_PATH}")
    
    # Lecture avec gestion des erreurs de format
    df = pd.read_csv(DATA_PATH, encoding='utf-16')
    logging.info(f"Fichier chargé. {len(df)} lignes détectées.")
    
    # Nettoyage : Conversion forcée en numérique
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
    
    # Séparation données valides / erreurs
    valid_df = df[(df['price'] > 0) & (df['quantity'] > 0)].copy()
    error_df = df[(df['price'] <= 0) | (df['quantity'] <= 0)].copy()
    
    # Sauvegarde des erreurs
    error_df.to_csv(ERROR_PATH, index=False)
    logging.info(f"Nombre d'erreurs isolées : {len(error_df)}")
    
    # Calcul des KPIs
    total_revenue = (valid_df['price'] * valid_df['quantity']).sum()
    metrics = {
        "nb_commandes": int(len(valid_df)),
        "chiffre_affaires": float(total_revenue),
        "panier_moyen": float(total_revenue / len(valid_df)) if len(valid_df) > 0 else 0
    }
    
    logging.info(f"KPIs calculés : {metrics}")
    return metrics

def load_to_mongo(**kwargs):
    """
    Chargement sécurisé dans MongoDB via connexion directe pymongo.
    """
    ti = kwargs['ti']
    metrics = ti.xcom_pull(task_ids='process_data')
    
    if not metrics:
        raise ValueError("Aucune métrique trouvée via XCom. La tâche précédente a échoué.")
        
    # Connexion directe à MongoDB (nom du service défini dans docker-compose)
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    
    try:
        db = client['ecommerce_analytics']
        collection = db['sales_metrics']
        
        document = {
            "execution_date": datetime.now().isoformat(),
            "dag_id": "ecommerce_sales_pipeline",
            "global_metrics": metrics
        }
        
        result = collection.insert_one(document)
        logging.info(f"Données insérées dans MongoDB avec ID : {result.inserted_id}")
    finally:
        client.close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    'ecommerce_sales_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    wait_for_file = FileSensor(
        task_id='wait_for_file',
        filepath='/opt/airflow/data/dataset.csv',
        fs_conn_id='fs_default', 
        poke_interval=10, 
        timeout=600
    )

    process_data = PythonOperator(
        task_id='process_data',
        python_callable=validate_and_process
    )

    load_to_mongodb = PythonOperator(
        task_id='load_to_mongodb',
        python_callable=load_to_mongo
    )

    wait_for_file >> process_data >> load_to_mongodb