import socket
import json
import psutil
import json
import requests
from scapy.all import *
from scapy import *
from scapy.tools import *
from scapy.layers.inet import *
from scapy.layers.l2 import *
import urllib.request
import pyshark

class Network:
    def __init__(self) -> None:
        pass

    def get_public_ip(self):
         return urllib.request.urlopen('https://ident.me').read().decode('utf8')

    def retrieve_host_ifaces(self):
        host_interfaces = socket.if_nameindex()
        counter=0
        inf_to_scan = []
        for index, inf in host_interfaces:
            #ignores first 3 interfaces returned in output. skipped interfaces irrelevant to scan.
            if counter != 3:
                counter+=1
            else:
                inf_to_scan.append(inf)
                print(str(index)+': '+ inf)
        
        if inf_to_scan != []:
            return inf_to_scan
        else:
            return None

    def open_tcp_ports(self):

        # Get all connections 
        connections = psutil.net_connections(kind='inet')
        ports = []

        # filter to get only ports equal to LISTEN
        my_ports = [conn.laddr.port for conn in connections if conn.status == psutil.CONN_LISTEN]

        # Exclude duplicate ports
        my_ports = list(set(my_ports))

        # Order from smallest to largest port
        my_ports.sort()

        # Show the TCP ports that is waiting for connection (LISTENING)
        for port in my_ports:
            ports.append(port)
            print(f"My Open TCP port= {port}  is LISTENING  for TCP connection", flush=True)

        if ports != []:
            return ports
        else:
            return None
            
       

        
        
        
    
        
         
