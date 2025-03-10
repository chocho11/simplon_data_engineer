# Utiliser une image Python légère comme base
FROM python:3.8-slim

# Installer le client NFS
RUN apt-get update && apt-get install -y nfs-common && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . /app

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Créer le point de montage pour NFS
RUN mkdir -p /mnt/nfs_share

# Ajouter des permissions pour le dossier partagé
RUN chmod 777 /mnt/nfs_share

# Exposer le port, si nécessaire
EXPOSE 5000

# Ajouter la tâche cron
RUN echo "0 11 * * * python3 /app/service1.py >> /var/log/service1.log 2>&1" > /etc/cron.d/service1-cron

# Donner les permissions nécessaires à cron
RUN chmod 0644 /etc/cron.d/service1-cron && \
    crontab /etc/cron.d/service1-cron

# Créer un fichier log pour cron
RUN touch /var/log/service1.log

# Lancer cron en mode foreground pour Docker
CMD ["cron", "-f"]
