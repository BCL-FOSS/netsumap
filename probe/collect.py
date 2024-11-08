#!/usr/bin/python

import scapy
import scapy.all
import scapy.tools
import socket
import sys
import json
import requests
import uuid
import sqlite3
import time
import os

USE_DB=True

if os.path.exists('probe.db') == False:
    conn = sqlite3.connect('probe.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE pbdata(id, status, host_ip, core_ip)")
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is None:
        print('Failed to create table in db ')
        USE_DB=False
    
def gen_id():
        try:
            id = uuid.uuid4()
        except Exception as e:
            return print("Probe ID Gen Failed")   
        return str(id)

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
        #ignores first 3 interfaces returned in output. skipped interfaces irrelevant to scan.
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

        core_url = url+"/netmetadata"
        payload = json.dumps(packet_data)
        make_request(url=core_url, payload=payload)

    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)

    print("Hostname of probe server:" + hostname)
    print("Probe Server IP:" + ip_addr)
        
def register(url=''):
    conn = sqlite3.connect('probe.db')
    cur = conn.cursor()
    probe_status = cur.execute("SELECT status FROM pbdata")

    if probe_status is None:
        print('Performing initial configuration of netsumap probe...')
        time.sleep(1.5)
        probe_id = gen_id()
        config_status = True

        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)

        print("Hostname of probe server:" + hostname)
        print("Probe Server IP:" + ip_addr)

        register_url = url+'/register'

        probe_obj = {
                "id": probe_id,
                "probe_data":{"hst_nm": hostname,
                            "ip": ip_addr}
            }

        probe_json = json.dumps(probe_obj)

        make_request(url=register_url,payload=probe_json)

        if USE_DB == True:
            cur.execute("INSERT INTO pbdata (probe_id, config_status, ip_addr, url) VALUES (?, ?, ?)", (probe_id, config_status, ip_addr, url))
            conn.commit()

        print('Probe configuration complete')
    else:
         print('Probe already configured')
         pass

def main(url='', count=0):
    register(url=url)
    net_scan(url=url, count=count)
    
if __name__ == "__main__":
    url = sys.argv[1]
    pcap_count = int(sys.argv[2])
    main(url=url, count=pcap_count)


    

