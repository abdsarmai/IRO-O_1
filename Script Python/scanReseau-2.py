#!/usr/bin/python3
import json
import mysql.connector
import subprocess
import socket

def get_name_from_ip(ip):
    if ip.endswith(".254"):
        return "routeur"	
    if ip.endswith("IMP"):
        return "Imprimante"

    pc_ips = ["172.20.30.126", "172.20.30.140", "172.20.30.121"]
    if ip in pc_ips:
        return "pc"

    ip_to_name_mapping = {
        "172.20.30.126": "PC-17",
        "172.20.30.140": "PC-17",
        "172.20.30.121": "PC-17"
    }
    
    if ip in ip_to_name_mapping:
        return ip_to_name_mapping[ip]

    try:
        nom_hote, _, _ = socket.gethostbyaddr(ip)
        return nom_hote
    except socket.herror:
        return "PC"

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
                    postes.append({"nom": nom, "ip": ip, "mac": mac})
        
        return postes
    except Exception as e:
        print(f"Erreur lors du scan du réseau : {e}")
        return []

def inserer_postes_json(postes):
    data = {"postes": postes}

    with open("postes.json", "w") as json_file:
        json.dump(data, json_file)

def inserer_postes_mysql(postes):
    connection = mysql.connector.connect(
        host="localhost",
        user="superviseur",
        password="azerty",
        database="RESEAU_LISSER"
    )
    cursor = connection.cursor()

    cursor.execute("DELETE FROM element")

    for poste in postes:
        cursor.execute("INSERT INTO element (nom, ip, mac) VALUES (%s, %s, %s)",
                       (poste["nom"], poste["ip"], poste["mac"]))
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    postes_detectes = scan_reseau()
    
    inserer_postes_mysql(postes_detectes)
    print(f"{len(postes_detectes)} postes ont été détectés et enregistrés dans la base de données.")

    inserer_postes_json(postes_detectes)
    print(f"Les informations des postes ont été enregistrées dans le fichier JSON.")
