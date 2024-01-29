#!/usr/bin/python3
import json
import subprocess

def scan_reseau():
    try:
        resultat = subprocess.check_output(["/usr/sbin/arp", "-a"]).decode("utf-8")
        lignes = resultat.split("\n")
        ip_addresses = []

        for ligne in lignes:
            if "incomplet" not in ligne:
                elements = ligne.split()
                if len(elements) >= 4:
                    ip = elements[1][1:-1]
                    ip_addresses.append(ip)
        
        return ip_addresses
    except Exception as e:
        print(f"Erreur lors du scan du réseau : {e}")
        return []

def generer_page_php(ip_addresses):
    with open("afficher_adresses.php", "w") as php_file:
        php_file.write("<!DOCTYPE html>\n")
        php_file.write("<html lang=\"en\">\n")
        php_file.write("<head>\n")
        php_file.write("    <meta charset=\"UTF-8\">\n")
        php_file.write("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
        php_file.write("    <title>Affichage des adresses IP</title>\n")
        php_file.write("</head>\n")
        php_file.write("<body>\n")
        php_file.write("    <h1>Adresses IP détectées</h1>\n")
        php_file.write("    <ul>\n")

        for ip in ip_addresses:
            php_file.write(f"        <li>{ip}</li>\n")

        php_file.write("    </ul>\n")
        php_file.write("</body>\n")
        php_file.write("</html>\n")

if __name__ == "__main__":
    ip_addresses_detectees = scan_reseau()
    
    generer_page_php(ip_addresses_detectees)
    print(f"{len(ip_addresses_detectees)} adresses IP ont été détectées et la page PHP a été générée.")
