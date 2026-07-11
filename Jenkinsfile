pipeline {
    agent any 
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                // Utilisation d'un venv pour isoler les dépendances proprement
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    
                    # Option B : Utilisation des contraintes officielles pour garantir la compatibilité
                    # On utilise ici une version stable (ex: 3.11). 
                    # Note : Si votre agent Jenkins force Python 3.14, cela peut rester complexe.
                    # L'idéal est de viser le fichier constraints correspondant à votre version.
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