#!/usr/bin/python3
import mysql.connector
import subprocess
import socket
from scapy.all import ARP, Ether, srp

def get_mac(ip):
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    if result:
        return result[0][1].src
    else:
        return None

def scan_reseau():
    try:
        resultat = subprocess.check_output(["/usr/sbin/arp", "-a"]).decode("utf-8")
        lignes = resultat.split("\n")
        postes = []
        pc_count = 1

        for ligne in lignes:
            if "incomplet" not in ligne:
                elements = ligne.split()
                if len(elements) >= 4:
                    ip = elements[1][1:-1]
                    mac = get_mac(ip)

                    try:
                        nom_appareil, _, _ = socket.gethostbyaddr(ip)
                    except socket.herror:
                        nom_appareil = ""

                    if nom_appareil == "":
                        if ip.endswith(".254") or "gateway" in ligne.lower():
                            nom_appareil = "Routeur"
                        else:
                            nom_appareil = f"PC-{pc_count}"
                            pc_count += 1
                    
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
