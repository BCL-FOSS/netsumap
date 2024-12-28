#!/usr/bin/python

import json
import requests
import sqlite3
import time
import os
from models.Network import Network
from models.Probe import Probe
import argparse

USE_DB=True

probe_cfg = Probe()
main_network = Network()

def initialize_database():
    if os.path.exists('probe.db') == False:
        conn = sqlite3.connect('probe.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE pbdata(id, host_ip, hostname, core_url)")
        res = cur.execute("SELECT name FROM sqlite_master")
        if res.fetchone() is None:
            print('Failed to create table in db ')
            USE_DB=False

        conn.commit()
        conn.close()
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
        
def enroll(url=''):
    conn = sqlite3.connect('probe.db')
    cur = conn.cursor()
    probe_status = cur.execute("SELECT id FROM pbdata")

    if probe_status.fetchall() == []:
        print('Performing initial configuration of netsumap probe...')
        time.sleep(1.5)
        probe_id, hostname = probe_cfg.gen_probe_register_data()
        external_ip = main_network.get_public_ip()
        ports = main_network.open_listening_ports()
        ifaces = main_network.get_ifaces()

        print(ifaces, flush=True)

        enroll_url = url+'/enroll'

        probe_obj = {
                        "id": probe_id,
                        "hst_nm": hostname,
                        "ip": external_ip,
                        "ports": str(ports),
                        "ifaces": str(ifaces)
                    }

        response = make_request(url=enroll_url, probe_json=probe_obj)

        
        print(json.dumps(response))

        if USE_DB == True:
            cur.execute("INSERT INTO pbdata (id, host_ip, hostname, core_url) VALUES (?, ?, ?, ?)", (probe_id, external_ip, hostname, url))
            conn.commit()
            
        #print(probe_id)
        print('Probe configuration complete')
        conn.close()
    else:
         print('Probe already configured')
         pass

def unenroll():
    print('Removing probe configuration...')
    conn = sqlite3.connect('probe.db')
    cur = conn.cursor()

    search_result = cur.execute("SELECT url FROM pbdata")
    core_url = search_result.fetchone()
    if core_url is not None:
        unenroll_url = core_url+'/unenroll'
        print(unenroll_url)
        
        response = make_request(url=unenroll_url, probe_json=probe_obj)
        
        cur.execute("DELETE FROM pbdata")
        conn.commit()
        print('Probe configuration removed.')
    else:
        print('No probe configuration found.')
    conn.close()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", action="store_true")
    parser.add_argument("--enroll", action="store_true")
    parser.add_argument("--unenroll", action="store_true")

    args = parser.parse_args()

    initialize_database()

    if args.enroll:
        url = args.url
        enroll(url=url)
    elif args.unenroll:
        unenroll()
    else:
        print("No valid action specified. Use --enroll or --unenroll.")


    