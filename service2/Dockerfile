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
