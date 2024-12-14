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
        
    def get_ifaces(self):
        try:
            # Execute the `ip link show` command to list all interfaces
            result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True, check=True)
            
            # Parse the output to extract interface names
            interfaces = []
            for line in result.stdout.splitlines():
                # Interface names appear after the line number and a colon
                if line and line[0].isdigit():
                    interface_name = line.split(':')[1].strip()
                    # Ignore interfaces like 'lo' if desired
                    interfaces.append(interface_name)

            return interfaces
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving interfaces: {e}")
            return []

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
        
    def open_listening_ports(self):
        # Get all connections for both TCP and UDP
        connections = psutil.net_connections(kind='inet') + psutil.net_connections(kind='inet4') + psutil.net_connections(kind='inet6')

        ports = []

        # Filter connections to get ports with status LISTEN (TCP) or listening UDP sockets
        listening_ports = [
            conn.laddr.port 
            for conn in connections 
            if conn.status == psutil.CONN_LISTEN or conn.type == psutil.SOCK_DGRAM
        ]

        # Exclude duplicate ports
        listening_ports = list(set(listening_ports))

        # Order from smallest to largest port
        listening_ports.sort()

        # Display and store the listening ports
        for port in listening_ports:
            ports.append(port)
            print(f"Open port {port} is LISTENING for connections", flush=True)

        return ports if ports else None
            
       

        
        
        
    
        
         
