pipeline {
    agent any
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install Dependencies') { 
            steps { sh 'pip install -r requirements.txt' } 
        }
        stage('Run Tests') { 
            steps { sh 'pytest tests/' } 
        }
        stage('Validate DAG') { 
            steps { sh 'python -m py_compile dags/*.py' } 
        }
    }
}