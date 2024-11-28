import json
import requests
import time
import json
import requests

class NetsumapCoreConn:
    def __init__(self) -> None:
        pass

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
             
    async def register(self, url='', public_ip="", id="", hostname="", ports=[]):
        print('Performing initial configuration of netsumap probe...', flush=True)
        time.sleep(1.5)
        probe_id=id
        external_ip=public_ip
        hostname=hostname

        register_url = url+'/register'

        probe_obj = {
                    "id": probe_id,
                    "hst_nm": hostname,
                    "ip": external_ip,
                    "ports": str(ports)

                }

        response = self.make_request(url=register_url, payload=probe_obj)

        if response is None:
            print("Probe registration failed. Verify your netsumap-core instance is running. Exiting probe initialization...", flush=True)
            return
        else:
            print(json.dumps(response), flush=True)
            print('Probe configuration complete', flush=True)
            
            
     