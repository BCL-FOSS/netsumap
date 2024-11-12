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
import urllib.request

USE_DB=True

if os.path.exists('probe.db') == False:
    conn = sqlite3.connect('probe.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE pbdata(id, status, host_ip, hostname)")
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is None:
        print('Failed to create table in db ')
        USE_DB=False
else:
     print("Probe DB already exists")
    
def gen_id():
        try:
            id = uuid.uuid4()
        except Exception as e:
            return print("Probe ID Gen Failed")   
        return str(id)

def make_request(url='', probe_json={}):

    payload = json.dumps(probe_json)

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
                print("Request successful.")
        else:
                print(f"Request failed with status code: {response.status_code}")

        return response.json()

    except Exception as e:
            print("Error occurred during request:", str(e))
            return None
    finally:
         response.close()
        
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
        response = make_request(url=core_url, payload=payload)

        print(json.loads(response.json()))

def register(url=''):
    conn = sqlite3.connect('probe.db')
    cur = conn.cursor()
    probe_status = cur.execute("SELECT status FROM pbdata")

    if probe_status.fetchall() == []:
        print('Performing initial configuration of netsumap probe...')
        time.sleep(1.5)
        id=gen_id()
        probe_id="nmp"+id
        config_status=True
        external_ip=urllib.request.urlopen('https://ident.me').read().decode('utf8')
        hostname=socket.gethostname()

        register_url = url+'/register'

        probe_obj = {
                "id": probe_id,
                "hst_nm": hostname,
                "ip": external_ip
            }

        response = make_request(url=register_url, probe_json=probe_obj)

        print(json.dumps(response))

        if USE_DB == True:
            cur.execute("INSERT INTO pbdata (id, status, host_ip, hostname) VALUES (?, ?, ?, ?)", (id, config_status, external_ip, hostname))
            conn.commit()

        #print(probe_id)
        print('Probe configuration complete')
    else:
         print('Probe already configured')
         pass

def main(url='', count=0):
    register(url=url)
    # net_scan(url=url, count=count)
    
if __name__ == "__main__":
    url = sys.argv[1]
    pcap_count = int(sys.argv[2])
    main(url=url, count=pcap_count)


    

