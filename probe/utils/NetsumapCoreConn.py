import socket
import json
import requests
import uuid
import sqlite3
import time
import urllib.request
from api_utils.API import API

class NetsumapCoreConn:
    def __init__(self) -> None:
        pass

    def gen_id(self):
        id = uuid.uuid4()
        if id:
            return str(id)
        else:
            return print("Probe ID Gen Failed")    
             
    def register(self, url='', USE_DB=True):
        conn = sqlite3.connect('probe.db')
        cur = conn.cursor()
        probe_status = cur.execute("SELECT status FROM pbdata")

        if probe_status.fetchall() == []:
            print('Performing initial configuration of netsumap probe...')
            time.sleep(1.5)
            id=self.gen_id()
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

            response = API.make_request(url=register_url, payload=probe_obj)

            print(json.dumps(response))

            if USE_DB == True:
                cur.execute("INSERT INTO pbdata (id, status, host_ip, hostname) VALUES (?, ?, ?, ?)", (id, config_status, external_ip, hostname))
                conn.commit()

            print('Probe configuration complete')
        else:
            print('Probe already configured')
            pass