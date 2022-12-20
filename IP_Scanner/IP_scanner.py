#!/usr/bin/env python
#IP scanner
import scapy.all as scapy
import optparse


def get_arguments():
   parser = optparse.OptionParser()

   parser.add_option("-t", "--target", dest="ip_address", help="interface to change it's mac address")

   (options, arguments) = parser.parse_args()
   if not options.ip_address:
       # code to handle error
       parser.error("[-] please specify an IP address or a range to scan, use --help for more info")

   return options


def scan(ip):
   arp_request = scapy.ARP(pdst=str(ip))
   broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
   arp_request_broadcast = broadcast/arp_request
   answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

   client_list = []
   for element in answered_list:
      client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
      client_list.append(client_dict)

   return client_list


def print_results(results_list):
   print("IP\t\t\tMAC Address\n--------------------------------------------------")
   for client in results_list:
      print(client["ip"] + "\t\t" + client['mac'])

options_2 = get_arguments()
scan_result = scan(options_2.ip_address)
print_results(scan_result)
