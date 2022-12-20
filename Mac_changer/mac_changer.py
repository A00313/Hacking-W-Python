#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
   parser = optparse.OptionParser()

   parser.add_option("-i", "--interface", dest="interface", help="interface to change it's mac address")
   parser.add_option("-m", "--mac", dest="new_mac", help="new mac address")

   (options, arguments) = parser.parse_args()
   if not options.interface:
       # code to handle error
       parser.error("[-] please specify an interface, use --help for more info")
   elif not options.new_mac:
       # code to handle error
       parser.error("[-] please specify a new mac, use --help for more info")
   return options

def change_mac(interface, new_mac):
   print("[+] Changing MAC address for " + interface + " to " + new_mac)
   # subprocess.call("ifconfig " + interface + " down", shell=True)
   # subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
   # subprocess.call("ifconfig " + interface + " up", shell=True)
   subprocess.call(["ifconfig", interface, "down"])
   subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
   subprocess.call(["ifconfig", interface, "up"])


def find_mac(interface):
   ifconfig_result = subprocess.check_output(["ifconfig", interface])
   # print(ifconfig_result)
   mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
   if mac_address_search_result:
       return mac_address_search_result.group(0)
   else:
       print("[-] could not read mac address.")


options_2 = get_arguments()
current_mac = find_mac(options_2.interface)
print("current MAC " + str(current_mac))
change_mac(options_2.interface, options_2.new_mac)
current_mac = find_mac(options_2.interface)
if current_mac == options_2.new_mac:
   print("[+] Mac address was successfully changed to " + current_mac)
else:
   print("[-] MAC address did not change.")
