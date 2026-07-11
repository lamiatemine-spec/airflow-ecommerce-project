pipeline {
    agent {
        docker { 
            image 'apache/airflow:2.9.0-python3.11' 
            args '-u root' 
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
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest tests/'
            }
        }
        stage('Validate DAG') {
            steps {
                sh 'python -m py_compile dags/*.py'
            }
        }
    }
}