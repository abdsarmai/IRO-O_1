import scapy.all as scapy
import socket
import mysql.connector

def get_device_info(ip):
    try:
        host_name = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        host_name = f"PC-{ip.split('.')[-1]}"

    mac_address = get_mac_address(ip)

    return {
        "Nom de l'appareil": host_name,
        "Adresse IP": ip,
        "Adresse MAC": mac_address
    }

def get_mac_address(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        return None

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices_list = []
    for element in answered_list:
        device_info = get_device_info(element[1].psrc)
        devices_list.append(device_info)

    return devices_list

def inserer_postes(postes):
    connection = mysql.connector.connect(
        host="localhost",
        user="adminJonathan",
        password="azerty",
        database="RESEAU_IRO_O"
    )
    cursor = connection.cursor()

    cursor.execute("DELETE FROM element")

    for device in postes:
        cursor.execute("INSERT INTO element (nom, ip, mac) VALUES (%s, %s, %s)", 
                       (device["Nom de l'appareil"], device["Adresse IP"], device["Adresse MAC"]))

    connection.commit()
    cursor.close()
    connection.close()

def print_results(devices_list):
    print("PC:")
    for device in devices_list:
        if device["Adresse IP"].endswith(".254") or "_gateway" in device["Nom de l'appareil"]:
            print("  Routeur:")
            print_device_info(device)
        else:
            print_device_info(device)

def print_device_info(device):
    print(f"  Nom de l'appareil: {device['Nom de l'appareil']}")
    print(f"    Adresse IP: {device['Adresse IP']}")
    print(f"    Adresse MAC: {device['Adresse MAC']}")
    print()

if __name__ == "__main__":
    target_ip = "192.168.134.0/24"  # Remplacez cela par votre plage d'adresses IP
    scanned_devices = scan(target_ip)
    print_results(scanned_devices)
    
    # Appeler la fonction inserer_postes pour enregistrer les résultats dans la base de données
    inserer_postes(scanned_devices)
