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
            #if counter != 1:
            #    counter+=1
            #else:
            #    inf_to_scan.append(inf)
            #    print(str(index)+': '+ inf)
            inf_to_scan.append(inf)
            print(str(index)+': '+ inf)
        
        if inf_to_scan != []:
            return inf_to_scan
        else:
            return None
         

    def net_scan(self, url='', count=10):
        
        inf_to_scan = self.retrieve_host_ifaces()
        pcaps = sniff(iface=inf_to_scan, count=count, prn=lambda x: x.summary())

        for cap in pcaps:
            
            packet_data = {
                
                "net_evt": cap.show(dump=True)
            }

            core_url = url+"/netmetadata"
            payload = json.dumps(packet_data)
            response = self.make_request(url=core_url, payload=payload)

            print(json.loads(response.json()))

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
        
    def host_discovery_local(self, target_subnet="", intfce=""):
        # arping(net=target_subnet, timeout=2, verbose=1)
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=target_subnet), iface=intfce, timeout=2)
        
        ans.summary()
        unans.summary()
        

        devices = []

        for sent, received in ans:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})

        if devices != []:
             return devices
        else:
             return None
        
    def pcap_scan(self, iface='', count=0, pcap_path='', time_out=50):
        capture = pyshark.LiveCapture(interface=iface, output_file=pcap_path)

        try:
            for packet in capture.sniff_continuously(packet_count=count):
                if packet is not None:
                    print(packet, flush=True)
        except:
            pass
        finally:
            capture.close()
            


        #capture.sniff(packet_count=count, timeout=time_out)

        
        
        
    
        
         
