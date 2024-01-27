#!/usr/bin/env python3
import subprocess

def executer_commande(commande):
    try:
        resultat = subprocess.check_output(commande, shell=True, universal_newlines=True)
        return resultat
    except subprocess.CalledProcessError as e:
        return f"Erreur lors de l'exécution de la commande {commande}: {e.output}"

def main():
    commandes_scan_reseau = [
        "ip a",  # Commande pour afficher l'adresse IP du poste qui exécute le programme
        "nmap 172.20.37.0-254/24",  # Scan du réseau
        "nmap 172.20.37.0/24"  # Scan du sous-réseau
    ]

    for commande in commandes_scan_reseau:
        print("=" * 50)
        print(f"Exécution de la commande (cachée): {commande}")
        print("=" * 50)
        resultat = executer_commande(commande)
        print(f"Résultat de la commande:")
        print(resultat)
        print("=" * 50)  

if __name__ == "__main__":
    main()
