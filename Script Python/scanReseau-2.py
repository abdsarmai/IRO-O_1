#!/usr/bin/python3
import mysql.connector
import subprocess
import socket

def determine_nom(ip, mac):
    # Si l'adresse IP se termine par .254 ou contient "_gateway", attribuer le nom "Routeur"
    if ip.endswith(".254") or "_gateway" in ip:
        return "Routeur"

    # Si le nom d'hôte est trouvé, l'utiliser
    try:
        nom_appareil, _, _ = socket.gethostbyaddr(ip)
        return nom_appareil
    except socket.herror:
        # Si le nom n'est pas trouvé, attribuer le nom "PC-[e]"
        return f"PC-{len(postes) + 1}"

def scan_reseau():
    try:
        resultat = subprocess.check_output(["/usr/sbin/arp", "-a"]).decode("utf-8")
        lignes = resultat.split("\n")
        postes = []

        for ligne in lignes:
            if "incomplet" not in ligne:
                elements = ligne.split()
                if len(elements) >= 4:
                    ip = elements[1][1:-1]
                    mac = elements[3]
                    nom = determine_nom(ip, mac)
                    postes.append((nom, ip, mac))

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
