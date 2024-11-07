#!/usr/bin/python

import scapy
import scapy.all
import scapy.tools
import socket
import sys
import json
import requests

def make_request(url='', payload={'':''}):

    headers = {
        'Content-Type': 'application/json'
        }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
                print("Request successful.")
        else:
                print(f"Request failed with status code: {response.status_code}")

        response.close()
        return response

    except Exception as e:
            print("Error occurred during request:", str(e))
            return None
        
def net_scan(url='', count=10):
    host_interfaces = socket.if_nameindex()
    counter=0
    inf_to_scan = []
    for index, inf in host_interfaces:
        #ignores first 3 interfaces returned in output. irrelevant to scan.
        if counter != 3:
            counter+=1
        else:
            inf_to_scan.append(inf)
            print(str(index)+': '+ inf)

    pcaps = scapy.all.sniff(iface=inf_to_scan, count=count, prn=lambda x: x.summary())

    for cap in pcaps:
        
        packet_data = {
            "net_evt": cap.show(dump=True)
        }

        payload = json.dumps(packet_data)
        make_request(url=url, payload=payload)
       

def main(url='', count=0):
    net_scan(url=url, count=count)
    
if __name__ == "__main__":
    url = sys.argv[1]
    pcap_count = int(sys.argv[2])
    main(url=url, count=pcap_count)


    

