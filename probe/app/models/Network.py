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
import subprocess

class Network:
    def __init__(self) -> None:
        pass

    def get_public_ip(self):
         return urllib.request.urlopen('https://ident.me').read().decode('utf8')
        
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
        
    def open_listening_ports(self):
        # Retrieve UFW status with rules
        try:
            result = subprocess.run(['ufw', 'status'], capture_output=True, text=True, check=True)
            output = result.stdout
        except subprocess.CalledProcessError as e:
            print("Error retrieving UFW status:", e, flush=True)
            return None

        ports = []

        # Parse UFW output to extract open ports
        for line in output.splitlines():
            if 'ALLOW' in line:
                # Extract the port and protocol from the line
                parts = line.split()
                if len(parts) > 0:
                    rule = parts[0]
                    if "/" in rule:  # Format like '22/tcp'
                        port, protocol = rule.split("/")
                        ports.append(int(port))

        # Remove duplicates and sort ports
        ports = list(set(ports))
        ports.sort()

        # Display the ports
        for port in ports:
            print(f"Open port {port} is ALLOWED by UFW", flush=True)

        return ports if ports else None
        
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
        
    def send_csv(self, url, csv_filepath):

        try:
            with open(csv_filepath, 'rb') as file:
                files = {'file': (csv_filepath, file, 'text/csv')}
            
                headers = {
                    'Content-Type': 'text/csv'
                }
                response = requests.request("POST", url, headers=headers, files=files)

                if response.status_code == 200:
                    print("Request successful.")
                else:
                    print(f"Request failed with status code: {response.status_code}")

                return response.json()
        except FileNotFoundError:
            print(f"Error: The file {csv_filepath} does not exist.")
        except requests.RequestException as e:
            print(f"Error: Unable to send request to {url}. Details: {e}")
                


        #capture.sniff(packet_count=count, timeout=time_out)

        
        
        
    
        
         
