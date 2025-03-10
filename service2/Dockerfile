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
EXPOSE 5001

# Ajouter une tâche cron pour exécuter le script à 12h00 tous les jours
RUN echo "0 12 * * * python3 /app/service2.py >> /var/log/service2.log 2>&1" > /etc/cron.d/service2-cron

# Configurer les permissions nécessaires pour cron
RUN chmod 0644 /etc/cron.d/service2-cron && crontab /etc/cron.d/service2-cron

# Créer un fichier log pour suivre l'exécution du cron job
RUN touch /var/log/service2.log

# Lancer cron en mode "foreground"
CMD ["cron", "-f"]
