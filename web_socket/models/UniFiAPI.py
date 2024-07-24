import requests
import http.client
import json
import os,os.path
import pprint


class UniFiAPI:

    def __init__(self, controller_ip, controller_port, username, password):
        self.base_url = f"https://{controller_ip}:{controller_port}"
        self.username = username
        self.password = password
        self.token = None

    def authenticate(self):
        auth_url = f"{self.base_url}/api/login"
        payload = {"username": self.username, "password": self.password}

        try:
            response = requests.post(auth_url, json=payload, verify=True)
            if response.status_code == 200:
                data = response.json()
                #print(response.headers.get("Set-Cookie"))
                header_data = response.headers.get("Set-Cookie")
                unifises = str(header_data[0:41])
                #print(unifises)
                csrf = str(header_data[69:113])
                #print(csrf)
                session_token = csrf + unifises
                #print(session_token)
                self.token = session_token
                #print(self.token)
                
                print("Authentication successful!")
                return session_token
            else:
                print("Authentication failed. Status code:", response.status_code)
        except Exception as e:
            print("Error occurred during authentication:", str(e))

    def get_sitedpi_data(self):

        ubnt_token = self.authenticate()
        print(ubnt_token)

        payload = {'':''}
        headers = {
            'Cookie': ubnt_token
        }

        try:
            conn = http.client.HTTPSConnection("ubntdemo.netifidash.io", 8443)

            conn.request("GET", "/api/s/default/stat/sitedpi", payload, headers)
            res = conn.getresponse()
            data = res.read()

            print(data)
        except Exception as e:
            print("Error occurred during GET request to stadpi endpoint:", str(e))
        
        #Clean up
        conn.close()

    def get_stadpi_data(self):

        ubnt_token = self.authenticate()
        print(ubnt_token)

        payload = {'':''}
        headers = {
            'Cookie': ubnt_token
        }

        try:
            conn = http.client.HTTPSConnection("ubntdemo.netifidash.io", 8443)

            conn.request("GET", "/api/s/default/stat/stadpi", payload, headers)
            res = conn.getresponse()
            data = res.read()

            print(data)
        except Exception as e:
            print("Error occurred during GET request to stadpi endpoint:", str(e))

        #Clean up
        conn.close()

    def get_event_data(self):

        ubnt_token = self.authenticate()
        print(ubnt_token)

        payload = {'':''}
        headers = {
            'Cookie': ubnt_token
        }

        try:
            conn = http.client.HTTPSConnection("ubntdemo.netifidash.io", 8443)

            conn.request("GET", "/api/s/default/stat/event", payload, headers)
            res = conn.getresponse()
            data = json.loads(res.read())

            #pprint.pprint(data)
            nestedData = data['data']
            pprint.pprint(nestedData)
        except Exception as e:
            print("Error occurred during GET request to stadpi endpoint:", str(e))
        
        #Clean up
        conn.close()

    def get_alarm_data(self):

        ubnt_token = self.authenticate()
        print(ubnt_token)

        payload = {'':''}
        headers = {
            'Cookie': ubnt_token
        }

        try:
            conn = http.client.HTTPSConnection("ubntdemo.netifidash.io", 8443)

            conn.request("GET", "/api/s/default/stat/alarm", payload, headers)
            res = conn.getresponse()
            data = json.loads(res.read())

            #pprint.pprint(data)
            nestedData = data['data']
            pprint.pprint(nestedData)
        except Exception as e:
            print("Error occurred during GET request to stadpi endpoint:", str(e))
        
        #Clean up
        conn.close()


    def get_health_data(self):

        ubnt_token = self.authenticate()
        print(ubnt_token)

        payload = {'':''}
        headers = {
            'Cookie': ubnt_token
        }

        try:
            conn = http.client.HTTPSConnection("ubntdemo.netifidash.io", 8443)

            conn.request("GET", "/api/s/default/stat/health", payload, headers)
            res = conn.getresponse()
            data = json.loads(res.read())

            #pprint.pprint(data)
            nestedData = data['data']
            pprint.pprint(nestedData)
        except Exception as e:
            print("Error occurred during GET request to stadpi endpoint:", str(e))
        
        #Clean up
        conn.close()

    def get_site_stats(self):

        ubnt_token = self.authenticate()
        print(ubnt_token)

        payload = {'':''}
        headers = {
            'Cookie': ubnt_token
        }

        try:
            conn = http.client.HTTPSConnection("ubntdemo.netifidash.io", 8443)

            conn.request("GET", "/api/stat/sites", payload, headers)
            res = conn.getresponse()
            data = json.loads(res.read())

            #pprint.pprint(data)
            nestedData = data['data']
            pprint.pprint(nestedData)
        except Exception as e:
            print("Error occurred during GET request to stadpi endpoint:", str(e))
        
        #Clean up
        conn.close()

# For Testing
#if __name__ == "__main__":
