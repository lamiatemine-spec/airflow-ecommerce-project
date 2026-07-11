# Utilisation de l'image officielle Airflow 2.9.0
FROM apache/airflow:2.9.0

# 1. Installation des outils de build système
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. airflow
USER airflow

# 3. Copie des requirements
COPY --chown=airflow:root requirements.txt /requirements.txt

# 4. Installation des dépendances 
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.0/constraints-3.12.txt"