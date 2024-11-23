import socket
import json
import requests
import uuid
import sqlite3
import time
import json
import requests

class NetsumapCoreConn:
    def __init__(self) -> None:
        pass

    def gen_id(self):
        id = uuid.uuid4()
        if id:
            return str(id)
        else:
            return print("Probe ID Gen Failed")  

    def make_request(self, url='', payload={}):

        payload = json.dumps(payload)

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
             
    def register(self, url='', public_ip="", USE_DB=True, ports=[]):
        conn = sqlite3.connect('probe.db')
        cur = conn.cursor()
        probe_status = cur.execute("SELECT status FROM pbdata")

        if probe_status.fetchall() == []:
            print('Performing initial configuration of netsumap probe...')
            time.sleep(1.5)
            id=self.gen_id()
            probe_id="nmp"+id
            config_status=True
            external_ip=public_ip
            hostname=socket.gethostname()

            register_url = url+'/register'

            probe_obj = {
                    "id": probe_id,
                    "hst_nm": hostname,
                    "ip": external_ip,
                    "ports": str(ports)

                }

            response = self.make_request(url=register_url, payload=probe_obj)

            print(json.dumps(response))

            if USE_DB == True:
                cur.execute("INSERT INTO pbdata (id, status, host_ip, hostname) VALUES (?, ?, ?, ?)", (id, config_status, external_ip, hostname))
                conn.commit()

            print('Probe configuration complete')
        else:
            print('Probe already configured')
            pass