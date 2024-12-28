#!/usr/bin/python

import json
import requests
import sqlite3
from models.Network import Network
from models.Probe import Probe

USE_DB=True

probe_cfg = Probe()
main_network = Network()

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

def core_ping_pong(url=''):
    ping_url = url+'/pong'
    response = make_request(url=ping_url)
    print(response)

if __name__ == "__main__":
    conn = sqlite3.connect('probe.db')
    cur = conn.cursor()

    search_result = cur.execute("SELECT url FROM pbdata")
    core_url = search_result.fetchone()
    if core_url is not None:
         core_ping_pong(url=str(core_url))
    else:
        print('No probe configuration found.')
    conn.close()


   