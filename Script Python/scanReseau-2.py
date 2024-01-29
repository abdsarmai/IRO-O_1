#!/usr/bin/python3
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

def generer_page_php(postes):
    with open("afficher_postes.php", "w") as php_file:
        php_file.write("<!DOCTYPE html>\n")
        php_file.write("<html lang=\"en\">\n")
        php_file.write("<head>\n")
        php_file.write("    <meta charset=\"UTF-8\">\n")
        php_file.write("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
        php_file.write("    <title>Affichage des postes</title>\n")
        php_file.write("</head>\n")
        php_file.write("<body>\n")
        php_file.write("    <h1>Postes et routeurs détectés</h1>\n")
        php_file.write("    <h2>Postes</h2>\n")
        php_file.write("    <table border=\"1\">\n")
        php_file.write("        <tr><th>Nom</th><th>IP</th><th>MAC</th></tr>\n")

        for poste in postes:
            if poste['categorie'] == 'poste':
                php_file.write(f"        <tr><td>{poste['nom']}</td><td>{poste['ip']}</td><td>{poste['mac']}</td></tr>\n")

        php_file.write("    </table>\n")

        php_file.write("    <h2>Routeurs</h2>\n")
        php_file.write("    <table border=\"1\">\n")
        php_file.write("        <tr><th>Nom</th><th>IP</th><th>MAC</th></tr>\n")

        for poste in postes:
            if poste['categorie'] == 'routeur':
                php_file.write(f"        <tr><td>{poste['nom']}</td><td>{poste['ip']}</td><td>{poste['mac']}</td></tr>\n")

        php_file.write("    </table>\n")
        php_file.write("</body>\n")
        php_file.write("</html>\n")

if __name__ == "__main__":
    postes_detectes = scan_reseau()
    
    generer_page_php(postes_detectes)
    print(f"{len(postes_detectes)} postes et routeurs ont été détectés et la page PHP a été générée.")
