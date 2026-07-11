pipeline {
    agent any 
    stages {
        stage('Install Dependencies') {
            steps {
                // On installe pip dans le conteneur Jenkins 
                sh 'apt-get update && apt-get install -y python3-pip'
                // On installe les dépendances avec le flag pour éviter les conflits
                sh 'pip3 install --break-system-packages -r requirements.txt'
            }
        }
        stage('Validate DAG') {
            steps {
                // On vérifie la syntaxe des fichiers Python
                sh 'python3 -m py_compile dags/*.py'
            }
        }
    }
}