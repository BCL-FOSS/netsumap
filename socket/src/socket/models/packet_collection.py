import scapy
import scapy.all
import scapy.tools
import pandas as pd



def net_scan(iface=''):
    scapy.all.sniff(iface=iface, prn=lambda x: x.summary())
    pd.json_normalize()

if __name__ == "__main__":
    monitored_iface = input('Enter interface name for packet collection: ')
    net_scan(iface=monitored_iface)

