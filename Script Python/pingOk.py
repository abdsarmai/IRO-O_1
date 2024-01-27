#!/usr/bin/env python3
import subprocess

def ping_ok(hostname):
    try:
        result = subprocess.run(['ping', '-c', '1', hostname], capture_output=True, text=True, check=True)

        print(result.stdout)
        
        return result.returncode == 0

    except subprocess.CalledProcessError:
        print("Erreur lors de l'exécution de la commande ping.")
        return False

if __name__ == "__main__":
    adresse_poste_de_travail = "172.20.37.46" #Adresse IP du poste de Georges MAHOPP TS1SIO

    if ping_ok(adresse_poste_de_travail):
        print("Le ping vers le poste de travail a réussi.")
    else:
        print("Le ping vers le poste de travail a échoué.")
