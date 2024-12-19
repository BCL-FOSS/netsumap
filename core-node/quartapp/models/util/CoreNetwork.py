from scapy.all import *
from scapy import *
from scapy.tools import *
from scapy.layers.inet import *
from scapy.layers.l2 import *
import urllib.request
import socket

class Network:
    def __init__(self) -> None:
        pass

    def get_hostname():
        hostname = socket.gethostname()
        return hostname

    def get_public_ip(self):
        return urllib.request.urlopen('https://ident.me').read().decode('utf8')

    def check_service(self, ip='', host_name='', port_list=[]):
       check_result = sr(IP(dst=ip)/TCP(dport=port_list),inter=0.5,retry=-2,timeout=1)

       ans, unans = check_result
    
       return ans, unans
    
    def ack_scan(self, target="", ports=[]):
        # ACK Scan
        ans, unans = sr(IP(dst=target)/TCP(dport=ports,flags="A"))
        ans.summary( lambda s,r : r.sprintf("%IP.src% is alive") )
        unans.summary()

    def syn_scan(self, target="", ports=[]):
        # SYN Scan
        ans, unans = sr(IP(dst=target)/TCP(dport=ports,flags="S"))
        ans.summary( lambda s,r : r.sprintf("%IP.src% is alive") )
        unans.summary()

    def udp_scan(self, target="", ports=[]):
        # UDP Ping
        ans, unans = sr(IP(dst=target)/UDP(dport=ports))
        ans.summary( lambda s,r : r.sprintf("%IP.src% is alive") )
        unans.summary()

    def ip_scan(self, target=""):
        ans, unans = sr(IP(dst=target,proto=(0,255))/"SCAPY",retry=2)
        ans.summary()
        unans.summary()

    def arp_ping(self, target_subnet="", iface=""):
        # arping(net=target_subnet, timeout=2, verbose=1)
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=target_subnet), iface=iface, timeout=2)
        ans.summary()
        unans.summary()
    
    
    

   