pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    # Création de l'environnement virtuel
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    
                    # Installation d'Airflow avec les contraintes officielles
                    AIRFLOW_VERSION="2.9.0"
                    PYTHON_VERSION="3.11"
                    CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
                    
                    echo "Installation d'Airflow avec les contraintes : ${CONSTRAINT_URL}"
                    ./venv/bin/pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
                    
                    # Installation du reste des dépendances
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh './venv/bin/pytest tests/'
            }
        }
        stage('Validate DAG') {
            steps {
                // On utilise le python de l'environnement virtuel pour la validation
                sh './venv/bin/python3 -m py_compile dags/*.py'
            }
        }
    }
}