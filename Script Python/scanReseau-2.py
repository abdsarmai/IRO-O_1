#!/usr/bin/python3
import json
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

def generer_page_json(postes):
    data = {"postes": postes}

    with open("postes.json", "w") as json_file:
        json.dump(data, json_file)

if __name__ == "__main__":
    postes_detectes = scan_reseau()
    
    generer_page_json(postes_detectes)
    print(f"{len(postes_detectes)} postes et routeurs ont été détectés et le fichier JSON a été généré.")
