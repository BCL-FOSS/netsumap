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
from models.NetsumapCoreConn import NetsumapCoreConn
from models.Network import Network
from models.Probe import Probe

USE_DB=True

probe = Probe()
main_network = Network()
core_conn = NetsumapCoreConn()


if os.path.exists('probe.db') == False:
    conn = sqlite3.connect('probe.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE pbdata(id, host_ip, hostname)")
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is None:
        print('Failed to create table in db ')
        USE_DB=False
else:
     print("Probe DB already exists")

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
        
def register(url=''):
    conn = sqlite3.connect('probe.db')
    cur = conn.cursor()
    probe_status = cur.execute("SELECT status FROM pbdata")

    if probe_status.fetchall() == []:
        print('Performing initial configuration of netsumap probe...')
        time.sleep(1.5)
        probe_id, hostname = probe.gen_probe_register_data()
        external_ip = main_network.get_public_ip()
        ports = main_network.open_tcp_ports()

        register_url = url+'/register'

        probe_obj = {
                        "id": probe_id,
                        "hst_nm": hostname,
                        "ip": external_ip,
                        "ports": str(ports)
                    }

        response = core_conn.make_request(url=register_url, probe_json=probe_obj)

        print(json.dumps(response))

        if USE_DB == True:
            cur.execute("INSERT INTO pbdata (id, host_ip, hostname) VALUES (?, ?, ?, ?)", (probe_id, external_ip, hostname))
            conn.commit()

        #print(probe_id)
        print('Probe configuration complete')
    else:
         print('Probe already configured')
         pass

def main(url=''):
    register(url=url)
    
if __name__ == "__main__":
    url = sys.argv[1]
  
    main(url=url)


    