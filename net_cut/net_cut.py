#!/usr/bin/env python
import netfilterqueue


def process_packet(packet):
    print(packet)
    packet.drop()


# Creating an instance of a netfilterqueue object and placing it in variable called queue
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
