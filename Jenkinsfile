pipeline {
    agent any 
    stages {
        stage('Checkout') {
            steps {
                // Récupération du code source depuis GitHub
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                // 1. Installation des outils nécessaires
                sh 'apt-get update && apt-get install -y python3-pip python3-venv'
                
                // 2. Création de l'environnement virtuel et installation
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    
                    # Installation d'Airflow sans contrainte de version stricte
                    # pour laisser pip choisir la version compatible avec Python 3.14
                    ./venv/bin/pip install apache-airflow
                    
                    # Installation des dépendances du projet
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }
        stage('Run Tests') {
            steps {
                // Utilisation du pytest de l'environnement virtuel
                sh './venv/bin/pytest tests/'
            }
        }
        stage('Validate DAG') {
            steps {
                // Validation de la syntaxe Python
                sh 'python3 -m py_compile dags/*.py'
            }
        }
    }
}