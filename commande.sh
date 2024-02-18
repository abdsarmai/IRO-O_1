#!/bin/bash

# Vérification des droits d'administration
if [[ $EUID -ne 0 ]]; then
    echo "Ce script doit être exécuté en tant qu'administrateur" 
    exit 1
fi

if [ $# -ne 1 ]; then
    echo "Usage: $0 <fichier>"
    exit 1
fi

# Récupérer le nom d'utilisateur actuel
user=$(whoami)

# Mise à jour des dépôts
apt update

# Installation des paquets requis
apt install -y apache2 php mariadb-server php-mysql python3 python3-pip mysql-connector-python

# Vérification de l'installation
echo "Installation terminée."

#Autorisation sur le dossier apache
chmod a+w /var/www/html

#Copie des fichiers
cp /RSOPHP /var/www/html
cp /Script\ Python "$1" "/home/$user/"

