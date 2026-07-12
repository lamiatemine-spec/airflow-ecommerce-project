from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd
import os
import logging

# --- CONFIGURATION ---
MONGO_URI = "mongodb://admin:password@ecommerce_mongodb:27017/?authSource=admin"
DATA_PATH = "/opt/airflow/data/dataset.csv"
VALID_DATA_PATH = "/opt/airflow/data/valid_data.csv"
ERROR_PATH = "/opt/airflow/data/errors.csv"

# --- LOGIQUE MÉTIER ---
def check_file_status():
    """Branching : Vérifie la présence du fichier source."""
    return 'process_data' if os.path.exists(DATA_PATH) else 'handle_error'

def validate_and_process(**kwargs):
    """Traitement robuste : lecture, nettoyage et validation."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Fichier introuvable : {DATA_PATH}")
    
    # Lecture du CSV avec encodage forcé en utf-16 pour éviter les erreurs de lecture
    # Utilisation de sep=',' comme convenu dans votre fichier CSV
    df = pd.read_csv(DATA_PATH, sep=',', encoding='utf-16')
    df.columns = df.columns.str.strip()
    
    # Vérification présence colonne category
    if 'category' not in df.columns:
        raise KeyError(f"Colonne 'category' manquante. Colonnes présentes : {df.columns.tolist()}")

    # Nettoyage des données numériques
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
    
    # Isolation des données valides vs invalides
    valid_df = df[(df['price'] > 0) & (df['quantity'] > 0)].copy()
    error_df = df[(df['price'] <= 0) | (df['quantity'] <= 0)].copy()
    
    valid_df.to_csv(VALID_DATA_PATH, index=False)
    error_df.to_csv(ERROR_PATH, index=False)
    
    logging.info(f"Traitement terminé. {len(valid_df)} lignes valides.")
    return valid_df['category'].unique().tolist()

def load_to_mongo(**kwargs):
    """Chargement des indicateurs finaux."""
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    try:
        db = client['ecommerce_analytics']
        db['sales_metrics'].insert_one({
            "execution_date": datetime.now().isoformat(),
            "status": "Success",
            "processed_at": VALID_DATA_PATH
        })
        logging.info("Données insérées dans MongoDB avec succès.")
    finally:
        client.close()

# --- DAG ---
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('ecommerce_sales_pipeline', default_args=default_args, schedule_interval=None, catchup=False) as dag:

    wait_for_file = FileSensor(task_id='wait_for_file', filepath=DATA_PATH, timeout=600)
    
    branching = BranchPythonOperator(task_id='branching', python_callable=check_file_status)

    process_data = PythonOperator(task_id='process_data', python_callable=validate_and_process)

    handle_error = PythonOperator(task_id='handle_error', python_callable=lambda: logging.error("Flux interrompu : fichier absent."))

    load_to_mongodb = PythonOperator(task_id='load_to_mongodb', python_callable=load_to_mongo)

    final_report = PythonOperator(
        task_id='final_report',
        python_callable=lambda: logging.info("Pipeline global clôturé avec succès."),
        trigger_rule=TriggerRule.ALL_DONE
    )

    # --- ARCHITECTURE DÉPENDANCES ---
    wait_for_file >> branching >> [process_data, handle_error]
    process_data >> load_to_mongodb >> final_report