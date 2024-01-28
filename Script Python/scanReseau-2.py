#!/usr/bin/python3
import nmap
from scapy.all import ARP, Ether, srp

def scan_with_nmap(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')

    devices = []
    for host in nm.all_hosts():
        devices.append({
            'ip': host,
            'hostname': nm[host].hostname() if 'hostname' in nm[host] else ''
        })

    return devices

def get_mac_addresses(ip_range):
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for element in answered_list:
        devices.append({
            'ip': element[1].psrc,
            'mac': element[1].hwsrc
        })

    return devices

if __name__ == "__main__":
    # Spécifiez la plage d'adresses IP que vous souhaitez scanner
    target_ip_range = "192.168.1.1/24"

    nmap_results = scan_with_nmap(target_ip_range)
    arp_results = get_mac_addresses(target_ip_range)

    # Afficher les résultats
    print("Résultats de Nmap:")
    for device in nmap_results:
        print(f"IP: {device['ip']}, Hostname: {device['hostname']}")

    print("\nRésultats ARP:")
    for device in arp_results:
        print(f"IP: {device['ip']}, MAC: {device['mac']}")
