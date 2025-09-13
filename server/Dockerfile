# ----------------------------
# Stage 1: Build dependencies
# ----------------------------
FROM python:3.12-slim AS build

# Variables d'environnement pour éviter les .pyc et bufferisation
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Installer les dépendances système nécessaires (par ex. psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier uniquement requirements pour tirer parti du cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# ----------------------------
# Stage 2: Runtime
# ----------------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copier les dépendances depuis l’étape build
COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=build /usr/local/bin /usr/local/bin

# Copier ton code applicatif
COPY . .

# Exposer le port de l'API
EXPOSE 8000

# Lancer l'app avec gunicorn + uvicorn worker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "api.v1.app:app", "--bind", "0.0.0.0:8000"]
