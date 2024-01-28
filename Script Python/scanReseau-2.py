#!/usr/bin/python3
import mysql.connector
import subprocess
import socket

def get_name_from_ip(ip):
    try:
        # Utiliser une requête DNS inverse pour obtenir le nom d'hôte associé à l'adresse IP
        nom_hote, _, _ = socket.gethostbyaddr(ip)
        return nom_hote
    except socket.herror:
        # En cas d'erreur, renvoyer une chaîne générique
        return "PC"

def scan_reseau():
    try:
        resultat = subprocess.check_output(["/usr/sbin/arp", "-a"]).decode("utf-8")
        lignes = resultat.split("\n")
        postes = []

        # Dictionnaire pour stocker le nombre d'occurrences de chaque nom
        nom_occurrences = {}

        for ligne in lignes:
            if "incomplet" not in ligne:  # Ignorer les entrées incomplètes
                elements = ligne.split()
                if len(elements) >= 4:
                    ip = elements[1][1:-1]  # Supprimer les parenthèses autour de l'adresse IP
                    mac = elements[3]
                    nom = get_name_from_ip(ip)  # Obtenir le nom à partir de l'adresse IP

                    # Vérifier si le nom est déjà dans le dictionnaire
                    if nom in nom_occurrences:
                        nom_occurrences[nom] += 1
                        nom_complet = f"{nom}-{nom_occurrences[nom]}"
                    else:
                        nom_occurrences[nom] = 1
                        nom_complet = nom

                    postes.append((ip, mac, nom_complet))
        
        return postes
    except Exception as e:
        print(f"Erreur lors du scan du réseau : {e}")
        return []

def inserer_postes(postes):
    connection = mysql.connector.connect(
        host="localhost",
        user="superviseur",
        password="azerty",
        database="RESEAU_LISSER"
    )
    cursor = connection.cursor()

    cursor.execute("DELETE FROM element")

    for ip, mac, nom in postes:
        cursor.execute("INSERT INTO element (nom, ip, mac) VALUES (%s, %s, %s)", (nom, ip, mac))
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    postes_detectes = scan_reseau()
    inserer_postes(postes_detectes)
    print(f"{len(postes_detectes)} postes ont été détectés et enregistrés dans la base de données.")
