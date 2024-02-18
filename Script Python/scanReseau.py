#!/usr/bin/python3
import mysql.connector
import subprocess
import socket

def get_device_category(ip):
    if ip.endswith(".254") or "_gateway" in ip:
        return "routeur"
    else:
        return "poste"

def get_name_from_ip(ip):
    try:
        nom_hote, _, _ = socket.gethostbyaddr(ip)
        return nom_hote
    except socket.herror:
        return "Inconnu"

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
                    nom = get_name_from_ip(ip)
                    categorie = get_device_category(ip)
                    postes.append({"nom": nom, "ip": ip, "mac": mac, "categorie": categorie})
        
        return postes
    except Exception as e:
        print(f"Erreur lors du scan du réseau : {e}")
        return []

def inserer_donnees(postes):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="adminAbdallah",
            password="azerty",
            database="RESEAU_IRO_O"
        )
        cursor = connection.cursor()

        for poste in postes:
            cursor.execute("INSERT INTO element (nom, ip, mac) VALUES (%s, %s, %s)", 
                           (poste["nom"], poste["ip"], poste["mac"]))
        
        connection.commit()
        print(f"{len(postes)} postes et routeurs ont été détectés et les données ont été insérées dans la base de données.")
    
    except Exception as e:
        print(f"Erreur lors de l'insertion des données dans la base de données : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    postes_detectes = scan_reseau()
    
    inserer_donnees(postes_detectes)
