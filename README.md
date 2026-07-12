# Projet Data Engineering : Pipeline E-commerce

Ce projet a pour objectif d'industrialiser un pipeline de traitement de données e-commerce, de l'extraction jusqu'au stockage, en utilisant des outils de pointe pour l'automatisation et l'orchestration.

## Stack Technique
- **Orchestration** : Apache Airflow
- **CI/CD** : Jenkins
- **Conteneurisation** : Docker / Docker Compose
- **Stockage** : MongoDB
- **Versionnement** : Git[cite: 1]

## Architecture du Projet
airflow-ecommerce-project/
├── dags/
│   └── ecommerce_sales_pipeline.py  # Le DAG principal 
├── tests/
│   └── test_pipeline.py             # Scripts de tests unitaires 
├── data/
│   └── dataset.csv                  # Dataset réel 
├── scripts/
│   └── check_mongodb.py             # Script de vérification 
├── docker/                          # Dossier de configuration Docker
│   ├── jenkins_home/                # Persistance des données Jenkins
│   ├── mongodb_data/                # Persistance des données MongoDB
│   ├── Dockerfile                   # Pour Airflow
│   └── Dockerfile.jenkins           # Pour Jenkins
├── Jenkinsfile                      # Pipeline CI/CD 
├── requirements.txt                 # Dépendances Python 
├── README.md                        # Documentation du projet 
└── docker-compose.yml               # Orchestration des services 