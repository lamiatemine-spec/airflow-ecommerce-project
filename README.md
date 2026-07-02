# Projet Data Engineering : Pipeline E-commerce

Ce projet a pour objectif d'industrialiser un pipeline de traitement de données e-commerce, de l'extraction jusqu'au stockage, en utilisant des outils de pointe pour l'automatisation et l'orchestration.

## Stack Technique
- **Orchestration** : Apache Airflow
- **CI/CD** : Jenkins
- **Conteneurisation** : Docker / Docker Compose
- **Stockage** : MongoDB
- **Versionnement** : Git[cite: 1]

## Architecture du Projet
```text
airflow-ecommerce-project/
├── dags/                # DAGs Airflow
├── tests/               # Tests unitaires (pytest)
├── data/                # Dataset source
├── scripts/             # Scripts utilitaires
├── docker/              # Fichiers de configuration Docker
├── Jenkinsfile          # Pipeline CI/CD
├── requirements.txt     # Dépendances Python
└── README.md            # Documentation du projet