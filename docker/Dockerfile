# Utilisation de l'image officielle Airflow 2.9.0 avec Python 3.11 pour une stabilité maximale
FROM apache/airflow:2.9.0-python3.11

# 1. Installation des outils de build système et du client Docker
# Ajout de docker.io pour permettre à Jenkins de piloter le daemon Docker via le socket
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    docker.io \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Installation des dépendances Python
USER airflow
COPY --chown=airflow:root requirements.txt /requirements.txt

# 3. Installation des dépendances avec les contraintes officielles Airflow
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.0/constraints-3.11.txt"