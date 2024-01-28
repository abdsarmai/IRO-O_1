#!/usr/bin/python3
import mysql.connector
import subprocess

def get_name_from_ip(ip):
    if ip.endswith("IMP"):
        return "Imprimante"
    elif "gateway" in ip:
        return "Routeur"
    
    ip_to_name_mapping = {
        "172.20.30.126": "Ordinateur",
        "172.20.30.140": "Ordinateur",
        "172.20.30.121": "Ordinateur"
    }
    
    # Si l'adresse IP ne se termine pas par "IMP" et n'est pas un "gateway",
    # chercher dans la table de mapping.
    return ip_to_name_mapping.get(ip, "Inconnu")

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
                    nom = get_name_from_ip(ip)  # Obtenir le nom à partir de l'adresse IP
                    postes.append((ip, mac, nom))
        
        return postes
    except Exception as e:
        print(f"Erreur lors du scan du réseau : {e}")
        return []
