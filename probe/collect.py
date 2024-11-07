#!/usr/bin/python

import scapy
import scapy.all
import scapy.tools
import socket
import sys
import json
import requests
import sqlite3
import uuid

sql_db = sqlite3.connect('netsuprobe.db')
db_cur = sql_db.cursor()
db_cur.execute("CREATE TABLE probe_config(id, config_status, ip)") 
table = db_cur.execute("SELECT probe_config FROM sqlite_master")
table_verify = table.fetchone()

def gen_id():
        try:
            id = uuid.uuid4()
        except Exception as e:
            return print("ID Gen Failed")   
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

        core_url = url+"/netmetadata"
        payload = json.dumps(packet_data)
        make_request(url=core_url, payload=payload)
        

def register(url=''):
    prof_check = db_cur.execute("SELECT id FROM probe_config") 
    if prof_check is None:
        probe_id = gen_id()
        config_status = True

        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)

        print("Your Computer Name is:" + hostname)
        print("Your Computer IP Address is:" + ip_addr)

        db_cur.execute("INSERT INTO probe_config (probe_id, config_status, ip_addr) VALUES (?,?,?)", (probe_id, config_status, ip_addr)) 
        sql_db.commit()

        register_url = url+'/register'

        probe_obj = {
             "id": probe_id,
             "probe_data":{"hst_nm": hostname,
                           "ip": ip_addr}
        }

        probe_json = json.dumps(probe_obj)

        make_request(url=register_url,payload=probe_json)

    else:
        pass

def main(url='', count=0):

    if table_verify:
        print('Config DB creation successful.')
        pass
    else:
        print('Config DB creation failed.')
        return
    
    register(url=url)
    
    net_scan(url=url, count=count)
    
if __name__ == "__main__":
    url = sys.argv[1]
    pcap_count = int(sys.argv[2])
    ws_url= sys.argv[3]
    main(url=url, count=pcap_count)


    

