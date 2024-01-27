#!/usr/bin/python3
import mysql.connector
import subprocess
import socket  # Ajout de la bibliothèque socket

def scan_reseau():
    try:
        resultat = subprocess.check_output(["/usr/sbin/arp", "-a"]).decode("utf-8")
        lignes = resultat.split("\n")
        postes = []

        for ligne in lignes:
            if "incomplet" not in ligne:  # Ignorer les entrées incomplètes
                elements = ligne.split()
                if len(elements) >= 4:
                    ip = elements[1][1:-1]  # Supprimer les parenthèses autour de l'adresse IP
                    mac = elements[3]

                    # Résoudre le nom d'hôte associé à l'adresse IP
                    try:
                        nom_appareil, _, _ = socket.gethostbyaddr(ip)
                    except socket.herror:
                        nom_appareil = ""

                    postes.append((nom_appareil, ip, mac))
        
        return postes
    except Exception as e:
        print(f"Erreur lors du scan du réseau : {e}")
        return []

def inserer_postes(postes):
    connection = mysql.connector.connect(
        host="localhost",
        user="adminJonathan",
        password="azerty",
        database="RESEAU_IRO_O"
    )
    cursor = connection.cursor()

    cursor.execute("DELETE FROM element")

    for nom, ip, mac in postes:
        cursor.execute("INSERT INTO element (nom, ip, mac) VALUES (%s, %s, %s)", (nom, ip, mac))
    
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    postes_detectes = scan_reseau()
    inserer_postes(postes_detectes)
    print(f"{len(postes_detectes)} postes ont été détectés et enregistrés dans la base de données.")
