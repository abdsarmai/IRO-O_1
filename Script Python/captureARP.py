#!/usr/bin/env python3
import subprocess

arp_path = '/usr/sbin/arp'

procARP = subprocess.Popen([arp_path, '-a', '172.20.33.254'],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = procARP.communicate()
resultat = stdout.decode("utf-8")
infos = resultat.split(' ')

if infos[0] != 'arp:':
    nomHote = infos[0]
    adrIP = infos[1][1:-1]  # On supprime les parenthèses qui entourent l'adresse IP de l'hôte
    adrMAC = infos[3]
    
    # On remplace le nom de l'hôte par inconnu si celui-ci est inconnu (valeur ?).
    nomHote = 'inconnu' if nomHote == '?' else nomHote
    
    print("Nom : " + nomHote)
    print("Adresse IP : " + adrIP)
    print("Adresse MAC : " + adrMAC)
else:
    print(resultat)
