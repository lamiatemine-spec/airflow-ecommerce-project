import pytest
import os

# Test pour vérifier que le dossier dags existe bien
def test_dags_directory_exists():
    assert os.path.exists('dags'), "Le dossier dags/ doit exister"

# Test pour vérifier que le fichier DAG principal est présent
def test_dag_file_exists():
    assert os.path.exists('dags/ecommerce_sales_pipeline.py'), "Le fichier DAG est introuvable"

# Exemple de test pour une future fonction de calcul de KPIs
def test_placeholder_calculation():
    # Ce test pourra être enrichi avec la logique métier réelle
    result = 1 + 1
    assert result == 2