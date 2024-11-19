import json
import requests

class API:
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