#!/usr/bin/python3
import mysql.connector
import nmap
import socket
from datetime import datetime

def get_mac(ip):
    # Utiliser une méthode pour obtenir l'adresse MAC (par exemple, scapy)
    pass

def generate_pc_name():
    current_date = datetime.now().strftime('%y%m%d')
    return f"PC-{current_date}"

def scan_reseau():
    try:
        postes = []

        nm = nmap.PortScanner()
        nm.scan(hosts='192.168.1.0/24', arguments='-n -sP')

        for result in nm.all_hosts():
            ip = result['host']
            mac = get_mac(ip)

            try:
                nom_appareil, _, _ = socket.gethostbyaddr(ip)
            except socket.herror:
                nom_appareil = ""

            if nom_appareil == "":
                if result['status']['state'] == 'up':
                    if ip.endswith(".254") or "_gateway" in result['hostnames'][0]['name'].lower():
                        nom_appareil = "Routeur"
                    else:
                        nom_appareil = generate_pc_name()

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
