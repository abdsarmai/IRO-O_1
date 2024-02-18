#!/usr/bin/env python3
import subprocess

def ping_nok(hostname):
    try:
        result = subprocess.run(['ping', '-c', '1', hostname], capture_output=True, text=True, check=True)

        print(result.stdout)
        
        return result.returncode != 0

    except subprocess.CalledProcessError:
        print("Erreur lors de l'exécution de la commande ping.")
        return True  

if __name__ == "__main__":
    adresse_poste_inexistant = "192.168.17.250" # Adresse non attribuée au réseau IRO-O

    if ping_nok(adresse_poste_inexistant):
        print("Le ping vers le poste de travail inexistant a échoué.")
    else:
        print("Le ping vers le poste de travail inexistant a réussi.")
