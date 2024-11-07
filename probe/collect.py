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
import websocket

websocket.enableTrace(True)
ws = None

sql_db = sqlite3.connect('netsuprobe.db')
db_cur = sql_db.cursor()
table_name = 'probe-config'
id_row = 'id'
cfg_row = 'config_status'
db_cur.execute("CREATE TABLE %s(%s, %s)") % (table_name, id_row, cfg_row)
table = db_cur.execute("SELECT %s FROM sqlite_master") % table_name
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
        
def net_scan(url='', count=10, ws=None):
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
        try:
            ws.send(payload)
            ws.close()
        except Exception as e:
            print(e)
        

def register(url=''):
    prof_check = db_cur.execute("SELECT %s FROM %s") % (id_row, table_name)
    if prof_check is None:
        probe_id = gen_id()
        config_status = True

        db_cur.execute("""
            INSERT INTO %s VALUES
                (%s, %s)
            """) % (table_name, probe_id, config_status)
        sql_db.commit()

        register_url = url+'/register'

        probe_obj = {
             "id": probe_id,
             "probe_data":""
        }

        probe_json = json.dumps(probe_obj)

        make_request(url=register_url,payload=probe_json)

    else:
        pass

def main(url='', count=0, ws_url=''):

    if ws_url == '':
         print("Enter WS URL. Closing...")
         return
    
    ws=websocket.create_connection(ws_url)

    if ws is None:
         print('Verify websocket is running.')
         return

    if table_verify:
        print('Config DB creation successful.')
        pass
    else:
        print('Config DB creation failed.')
        return
    
    register(url=url)
    
    net_scan(url=url, count=count, ws=ws)
    
if __name__ == "__main__":
    url = sys.argv[1]
    pcap_count = int(sys.argv[2])
    ws_url= sys.argv[3]
    main(url=url, count=pcap_count, ws_url=ws_url)


    

