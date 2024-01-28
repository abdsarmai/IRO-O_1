#!/usr/bin/python3
import subprocess
import mysql.connector

def scan_reseau():
    resultat = subprocess.check_output(["arp", "-a"]).decode("utf-8")
    lignes = resultat.split("\n")
    postes = []

    for ligne in lignes:
        if "incomplet" not in ligne:
            elements = ligne.split()
            if len(elements) >= 4:
                ip = elements[1][1:-1]  # Correction de la récupération de l'adresse IP
                mac = elements[3]
                postes.append((ip, mac))

    return postes

def inserer_postes(postes):
    connection = mysql.connector.connect(
        host='localhost',
        user='superviseur',
        password='azerty',
        database='RESEAU_LISSER'
    )
    cursor = connection.cursor()

    # Supprimer les anciens éléments de la table avant d'insérer les nouveaux
    cursor.execute("DELETE FROM element")

    for poste in postes:
        # Utilisation d'une requête paramétrée pour éviter les injections SQL
        cursor.execute("INSERT INTO element (ip, mac) VALUES (%s, %s)", poste)

    # Valider les changements dans la base de données
    connection.commit()

    # Fermer la connexion
    cursor.close()
    connection.close()

# Exécution des fonctions
postes_reseau = scan_reseau()
inserer_postes(postes_reseau)
