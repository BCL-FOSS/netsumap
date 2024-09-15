import os,os.path
from models.util_models.Utility import Utility
import models.UbiquiPy

import aiohttp

error_codes = [460, 472, 489]

class UniFiNetAPI(UbiquiPy):

    def __init__(self, is_udm=False, **kwargs):
        self.base_url = f"https://{kwargs.get('controller_ip')}:{kwargs.get('controller_port')}"
        self.url = kwargs.get('controller_ip')
        self.inform_url = f"https://{kwargs.get('controller_ip')}:8080/inform"
        self.port = kwargs.get('controller_port')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.token = None
        self.is_udm = is_udm
        self.auth_check = False
        self.util_obj = Utility()
        #self.id = ''
        #self.name = ''
        #self.ubiquipy_client_session = aiohttp.ClientSession()
    
    def get_profile_data(self):
        return {
            "id": self.id,
            "profile_name": self.name,
            "base_url": self.base_url,
            "url": self.url,
            "inform_url": self.inform_url,
            "port" : self.port,
            "username": self.username,
            "token": self.token,
            "is_udm" : self.is_udm
        }
            
    async def authenticate(self):

        if self.is_udm is True:
            auth_url = f"{self.base_url}/proxy/network/api/auth/login"
        else:
            auth_url = f"{self.base_url}/api/login"

        payload = {"username": self.username, "password": self.password}

        async with self.ubiquipy_client_session as session:
            try:
                # Asynchronous POST request to UniFi API
                async with session.post(url=auth_url, json=payload) as response:
                    if response.status == 200:
                        #response_data = await response.json()
                        header_data = response.headers.getall('Set-Cookie', [])
                        for cookie in header_data:
                            if 'unifises' in cookie:
                               unifises_token = cookie.split(';')[0].split('=')[1]
                            if 'csrf_token' in cookie:
                                csrf_token = cookie.split(';')[0].split('=')[1]

                        unifises = str(unifises_token)
                        #print(unifises)
                        csrf = str(csrf_token)
                        #print(csrf)
                        session_token = "unifises="+unifises + ";"+ "csrf_token="+csrf + ";"
                        self.token = session_token
                        self.id = self.gen_id()
                        self.auth_check = True
                        response.close()
                        #print({"message": "Authentication successful", "data": response_data, "token": session_token, "id": self.id})
                        return self.get_profile_data()
                    else:
                        return {"message": "Authentication failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}


    async def sign_out(self):

        if self.is_udm is True:
            url = f"{self.base_url}/proxy/network/api/logout"
        else:
            url = f"{self.base_url}/api/logout"

        payload={"":""}

        headers={
                        'Content-Type':'application/json',
                        'Cookie':self.token
                    }   

        async with self.ubiquipy_client_session as session:
            try:
                # Asynchronous POST request to UniFi API
                async with session.post(url=url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        self.auth_check = False
                        response.close()
                        return {"message": "Signout successful", "data": response_data}
                    else:
                        return {"message": "Signout failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

            
    async def site_dpi_data(self, site='', type=False, cmd=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/sitedpi" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/sitedpi" % site

            url = f"{self.base_url}{url_string}"

        if type is False:
            payload = {'type': 'by_app'}
        else:
            payload = {'type': 'by_cat'}

        async with self.ubiquipy_client_session as session:
            try:
                match cmd.strip():
                    case 'p':
                        headers={
                            'Content-Type':'application/json',
                            'Cookie':self.token
                        }

                        async with session.post(url=url, json=payload, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    
                    case 'g':
                        headers={
                            'Cookie':self.token
                        }

                        async with session.get(url=url, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    case _:
                        return error_codes[1]                
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def client_dpi_data(self, site='', type=False, macs=[]):

        if type is False and macs != []:
            payload = {'type': 'by_app',
                       'macs': macs}
        elif type is True and macs != []:
            payload = {'type': 'by_cat',
                       'macs': macs}
        elif type is False:
            payload = {'type': 'by_app'}
        else:
            payload = {'type': 'by_cat'}

            
        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/stadpi" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/stadpi" % site

            url = f"{self.base_url}{url_string}"

        headers={
                        'Content-Type':'application/json',
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                # Asynchronous POST request to UniFi API
                async with session.post(url=url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def event_data(self, site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/event" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/event" % site

            url = f"{self.base_url}{url_string}"

        headers={
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                # Asynchronous POST request to UniFi API
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def alarm_data(self, site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/alarm" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/alarm" % site

            url = f"{self.base_url}{url_string}"

        headers={
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                # Asynchronous POST request to UniFi API
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def controller_health_data(self):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/default/stat/health"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/default/stat/health"

            url = f"{self.base_url}{url_string}"

        headers={
                        'Cookie':self.token
                    }   

        async with self.ubiquipy_client_session as session:
            try:
                # Asynchronous POST request to UniFi API
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        response.close()
                        return response_data
                    else:
                        return {"message": "Failed to retrieve controller health data", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def site_stats(self):

        if self.is_udm is True:

            url_string = "/proxy/network/api/stat/sites"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/stat/sites"

            url = f"{self.base_url}{url_string}"

        headers={
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                # Asynchronous POST request to UniFi API
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        response.close()
                        return response_data
                    else:
                        return {"message": "Failed to retrieve site stats", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def sites(self):

        if self.is_udm is True:

            url_string = "/proxy/network/api/self/sites"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/self/sites"

            url = f"{self.base_url}{url_string}"

        headers={
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        response.close()
                        return response_data
                    else:
                        return {"message": "Failed to retrieve sites", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}


    async def list_admins(self):

        if self.is_udm is True:

            url_string = "/proxy/network/api/stat/admin"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/stat/admin"

            url = f"{self.base_url}{url_string}"

        headers={
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        response.close()
                        return response_data
                    else:
                        return {"message": "Failed to retrieve admin profiles", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def udm_poweroff(self):

        
        if self.is_udm is True:

            url_string = "/proxy/network/api/system/poweroff"

            url = f"{self.base_url}{url_string}"
        else:
            return {"Controller Compatability Error":"This command does not work with self hosted controllers. Please reinitialize the object with is_udm=True and set the URL as the IP address of the UDM or hardware Cloud Gateway"}
            
        headers={
                        'Cookie':self.token
                    }  
        
        payload = {"":""}

        async with self.ubiquipy_client_session as session:
            try:
                async with session.post(url=url, headers=headers, payload=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        response.close()
                        return response_data
                    else:
                        return {"Command Error": "Failed to power off Cloud Gateway hardware.", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def udm_reboot(self):

        if self.is_udm is True:

            url_string = "/proxy/network/api/system/reboot"

            url = f"{self.base_url}{url_string}"
        else:
            return {"Controller Compatability Error":"This command does not work with self hosted controllers. Please reinitialize the object with is_udm=True and set the URL as the IP address of the UDM or hardware Cloud Gateway"}


        headers={
                    'Cookie':self.token
                }  
        
        payload = {"":""}

        async with self.ubiquipy_client_session as session:
            try:
                async with session.post(url=url, headers=headers, payload=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        response.close()
                        return response_data
                    else:
                        return {"Command Error": "Failed to reboot Cloud Gateway hardware.", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def get_sysinfo(self):

        if self.is_udm is True:
            url = f"{self.base_url}/proxy/network/api/s/default/stat/sysinfo"
        else:
            url = f"{self.base_url}/api/s/default/stat/sysinfo"

        headers={
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        response.close()
                        return response_data
                    else:
                        return {"message": "Failed to retrieve controller information", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def active_clients(self, site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/sta" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/sta" % site

            url = f"{self.base_url}{url_string}"

        headers={
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        response.close()
                        return response_data
                    else:
                        return {"message": "Failed to retrieve controller information", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def all_clients(self, cmd='', site=''):
        
        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/user" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/user" % site

            url = f"{self.base_url}{url_string}"

        payload = {'':''}

        headers={
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                # Asynchronous POST request to UniFi API
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def device_data_basic(self, site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/device-basic" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/device-basic" % site

            url = f"{self.base_url}{url_string}"

        headers={
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                # Asynchronous POST request to UniFi API
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def device_data(self, macs=[], site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/device" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/device" % site

            url = f"{self.base_url}{url_string}"

        async with self.ubiquipy_client_session as session:
            try:
                if self.is_udm is False and macs != []: 
                    payload = {'macs': macs}

                    headers={
                        'Content-Type':'application/json',
                        'Cookie':self.token
                    } 
                    async with session.post(url=url, headers=headers, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            nested_data = data['data']
                            response.close()
                            return nested_data
                        else:
                            return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    
                else:
                    headers={
                        'Cookie':self.token
                    }  
                    async with session.get(url=url, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            nested_data = data['data']
                            response.close()
                            return nested_data
                        else:
                            return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def site_settings(self, key='', id='', cmd='', site=''):

        if self.is_udm is True:

            if not any ((key, id)):

                url_string = "/proxy/network/api/s/%s/rest/setting/%s/%s" % (site, key, id)
            else:

                url_string = "/proxy/network/api/s/%s/rest/setting" % site       
        else:
            if not any ((key, id)):

                url_string = "/api/s/%s/rest/setting/%s/%s" % (site, key, id)
            else:

                url_string = "/api/s/%s/rest/setting" % site 

        url = f"{self.base_url}{url_string}"

        async with self.ubiquipy_client_session as session:
            try:
                match cmd.strip():
                    case 'e':
                        payload = {'': ''}
                        headers={
                        'Content-Type':'application/json',
                        'Cookie':self.token
                        } 
                        async with session.put(url=url, headers=headers, json=payload) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    case 'g':
                        headers={
                        'Cookie':self.token
                        } 
                        async with session.get(url=url, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    case _:
                        return error_codes[1]
                    
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def active_routes(self, site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/routing" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/routing" % site

            url = f"{self.base_url}{url_string}"

        headers={
                        'Cookie':self.token
                    }  

        async with self.ubiquipy_client_session as session:
            try:
                # Asynchronous POST request to UniFi API
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        response.close()
                        return response_data
                    else:
                        return {"message": "Failed to retrieve active routes", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def firewall_rules(self, cmd='', site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/firewallrule" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/firewallrule" % site

            url = f"{self.base_url}{url_string}"

        async with self.ubiquipy_client_session as session:
            try:
                match cmd.strip():
                    case 'e':
                        payload = {'': ''}
                        headers={
                        'Content-Type':'application/json',
                        'Cookie':self.token
                        } 
                        async with session.put(url=url, headers=headers, json=payload) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    case 'g':
                        headers={
                        'Cookie':self.token
                        } 
                        async with session.get(url=url, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    case _:
                        return error_codes[1]
                    
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def firewall_groups(self, cmd='', site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/firewallgroup" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/firewallgroup" % site

            url = f"{self.base_url}{url_string}"

        async with self.ubiquipy_client_session as session:
            try:
                match cmd.strip():
                    case 'e':
                        payload = {'': ''}
                        headers={
                        'Content-Type':'application/json',
                        'Cookie':self.token
                        } 
                        async with session.put(url=url, headers=headers, json=payload) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    case 'g':
                        headers={
                        'Cookie':self.token
                        } 
                        async with session.get(url=url, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    case _:
                        return error_codes[1]
                    
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def wlans(self, wlan_name='', psswd='', site_id='', wlan_id='', cmd='', site=''):

        payload = {
                "name": wlan_name,
                "password": psswd,
                "site_id": site_id,
                "usergroup_id": "660e8cf02260b651d2585910",
                "ap_group_ids": [
                    "660e8cf02260b651d2585914"
                ],
                "ap_group_mode": "all",
                "wpa_mode": "wpa2",
                "x_passphrase": psswd
            }
        
        async with self.ubiquipy_client_session as session:
            try:
                if self.is_udm is True:
                    match cmd.strip():
                        case 'e':
                            url_string = "/proxy/network/api/s/%s/rest/wlanconf/%s" % (site, wlan_id)

                            url = f"{self.base_url}{url_string}"

                            headers={
                                'Content-Type':'application/json',
                                'Cookie':self.token
                            } 
                            async with session.put(url=url, headers=headers, json=payload) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    nested_data = data['data']
                                    response.close()
                                    return nested_data
                                else:
                                    return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                            
                        case 'p':
                            url_string = "/proxy/network/api/s/%s/rest/wlanconfs" % site

                            url = f"{self.base_url}{url_string}"

                            headers={
                                'Content-Type':'application/json',
                                'Cookie':self.token
                            } 
                            async with session.post(url=url, headers=headers, json=payload) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    nested_data = data['data']
                                    response.close()
                                    return nested_data
                                else:
                                    return {"message": "Site DPI stat retrieval failed", "status_code": response.status}

                        case 'g':

                            url_string = "/proxy/network/api/s/%s/rest/wlanconfs" % site

                            url = f"{self.base_url}{url_string}"

                            headers={
                                'Cookie':self.token
                            } 
                            async with session.get(url=url, headers=headers) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    nested_data = data['data']
                                    response.close()
                                    return nested_data
                                else:
                                    return {"message": "Site DPI stat retrieval failed", "status_code": response.status}

                else:

                    match cmd.strip():

                        case 'e':

                            url_string = "/api/s/%s/rest/wlanconf/%s" % (site, wlan_id)

                            url = f"{self.base_url}{url_string}"

                            headers={
                                'Content-Type':'application/json',
                                'Cookie':self.token
                            } 
                            async with session.put(url=url, headers=headers, json=payload) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    nested_data = data['data']
                                    response.close()
                                    return nested_data
                                else:
                                    return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                        
                        case 'p':
                            url_string = "/api/s/%s/rest/wlanconfs" % site

                            url = f"{self.base_url}{url_string}"

                            url_string = "/proxy/network/api/s/%s/rest/wlanconfs" % site

                            url = f"{self.base_url}{url_string}"

                            headers={
                                'Content-Type':'application/json',
                                'Cookie':self.token
                            } 
                            async with session.post(url=url, headers=headers, json=payload) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    nested_data = data['data']
                                    response.close()
                                    return nested_data
                                else:
                                    return {"message": "Site DPI stat retrieval failed", "status_code": response.status}

                        case 'g':

                            url_string = "/api/s/%s/rest/wlanconfs" % site

                            url = f"{self.base_url}{url_string}"

                            headers={
                                'Cookie':self.token
                            } 
                            async with session.get(url=url, headers=headers) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    nested_data = data['data']
                                    response.close()
                                    return nested_data
                                else:
                                    return {"message": "Site DPI stat retrieval failed", "status_code": response.status}

            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def rogue_aps(self, seen_last=0, site=''):   

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/rogueap" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/rogueap" % site

            url = f"{self.base_url}{url_string}"

        
        async with self.ubiquipy_client_session as session:

            if seen_last != 0: 
                    
                payload = {'within': seen_last}

                try:
                    headers={
                            'Content-Type':'application/json',
                            'Cookie':self.token
                    } 
                    async with session.post(url=url, headers=headers, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            nested_data = data['data']
                            response.close()
                            return nested_data
                        else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                except aiohttp.ClientError as e:
                    return {"error": str(e), "status_code": 500}
                except Exception as error:
                    return {"error": str(error)}

            else:

                try:
                    headers={
                            'Cookie':self.token
                    } 
                    async with session.get(url=url, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            nested_data = data['data']
                            response.close()
                            return nested_data
                        else:
                            return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                except aiohttp.ClientError as e:
                    return {"error": str(e), "status_code": 500}
                except Exception as error:
                    return {"error": str(error)}

    async def dynamic_dns_info(self, site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/dynamicdns" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/dynamicdns" % site

            url = f"{self.base_url}{url_string}"

        
        async with self.ubiquipy_client_session as session:
            try:
                headers={
                            'Cookie':self.token
                } 
                async with session.get(url=url, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            nested_data = data['data']
                            response.close()
                            return nested_data
                        else:
                            return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                    return {"error": str(e), "status_code": 500}
            except Exception as error:
                    return {"error": str(error)}

    async def dynamic_dns_config(self, cmd='', site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/dynamicdns" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/dynamicdns" % site

            url = f"{self.base_url}{url_string}"

        match cmd.split():
            case 'e':
                payload = {'': ''}

                async with self.ubiquipy_client_session as session:
                    try:
                        headers={
                                'Cookie':self.token
                        } 
                        async with session.put(url=url, headers=headers, json=payload) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    except aiohttp.ClientError as e:
                            return {"error": str(e), "status_code": 500}
                    except Exception as error:
                            return {"error": str(error)}

            case 'g':
                async with self.ubiquipy_client_session as session:
                    try:
                        headers={
                                'Cookie':self.token
                        } 
                        async with session.get(url=url, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    except aiohttp.ClientError as e:
                            return {"error": str(e), "status_code": 500}
                    except Exception as error:
                            return {"error": str(error)}

    async def list_port_profiles(self, site=''):

        input_validation = self.input_validation([site])

        if input_validation == 0:
            return error_codes[0]

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/portconf" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/portconf" % site

            url = f"{self.base_url}{url_string}"

        async with self.ubiquipy_client_session as session:
            try:
                headers={
                    'Cookie':self.token
                } 
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def rf_scan_results(self, mac='', cmd='', site=''):
        payload = {'': ''}

        if self.is_udm is True:
            match cmd.strip():
                case 'd':
                    url_string = "/proxy/network/api/s/%s/stat/spectrumscan/%s" % (site, mac)

                    url = f"{self.base_url}{url_string}"

                    async with self.ubiquipy_client_session as session:
                        try:
                            headers={
                                    'Cookie':self.token
                            } 
                            async with session.get(url=url, headers=headers) as response:
                                if response.status == 200:
                                        data = await response.json()
                                        nested_data = data['data']
                                        response.close()
                                        return nested_data
                                else:
                                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                        except aiohttp.ClientError as e:
                                return {"error": str(e), "status_code": 500}
                        except Exception as error:
                                return {"error": str(error)}

                case 'g':
                    url_string = "/proxy/network/api/s/%s/stat/spectrumscan/" % site

                    url = f"{self.base_url}{url_string}"

                    async with self.ubiquipy_client_session as session:
                            try:
                                headers={
                                    'Cookie':self.token
                                } 
                                async with session.get(url=url, headers=headers) as response:
                                    if response.status == 200:
                                        data = await response.json()
                                        nested_data = data['data']
                                        response.close()
                                        return nested_data
                                    else:
                                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                            except aiohttp.ClientError as e:
                                return {"error": str(e), "status_code": 500}
                            except Exception as error:
                                return {"error": str(error)}
                        
        else:
            match cmd.strip():
                case 'd':
                    url_string = "/api/s/%s/stat/spectrumscan/%s" % (site, mac)

                    url = f"{self.base_url}{url_string}"

                    async with self.ubiquipy_client_session as session:
                        try:
                            headers={
                                    'Cookie':self.token
                            } 
                            async with session.get(url=url, headers=headers) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    nested_data = data['data']
                                    response.close()
                                    return nested_data
                                else:
                                    return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                        except aiohttp.ClientError as e:
                            return {"error": str(e), "status_code": 500}
                        except Exception as error:
                            return {"error": str(error)}

                case 'g':
                    url_string = "/api/s/%s/stat/spectrumscan/" % site

                    url = f"{self.base_url}{url_string}"

                    async with self.ubiquipy_client_session as session:
                        try:
                            headers={
                                    'Cookie':self.token
                            } 
                            async with session.get(url=url, headers=headers) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    nested_data = data['data']
                                    response.close()
                                    return nested_data
                                else:
                                    return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                        except aiohttp.ClientError as e:
                            return {"error": str(e), "status_code": 500}
                        except Exception as error:
                            return {"error": str(error)}

    async def radius_profiles(self, cmd='', site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/radiusprofile" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/radiusprofile" % site

            url = f"{self.base_url}{url_string}"

        match cmd.strip():
            case 'e':
                payload = {'': ''}

                async with self.ubiquipy_client_session as session:
                    try:
                        headers={
                                'Content-Type':'application/json',
                                'Cookie':self.token
                        }
                            
                        async with session.put(url=url, headers=headers, json=payload) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    except aiohttp.ClientError as e:
                        return {"error": str(e), "status_code": 500}
                    except Exception as error:
                        return {"error": str(error)}
                       
            case 'p':
                payload = {'': ''}
                    

                async with self.ubiquipy_client_session as session:
                    try:
                        headers={
                                'Content-Type':'application/json',
                                'Cookie':self.token
                        }
                            
                        async with session.post(url=url, headers=headers, json=payload) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    except aiohttp.ClientError as e:
                        return {"error": str(e), "status_code": 500}
                    except Exception as error:
                        return {"error": str(error)}


                       
            case 'g':
                async with self.ubiquipy_client_session as session:
                    try:
                        headers={
                            'Cookie':self.token
                        } 
                        async with session.get(url=url, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    except aiohttp.ClientError as e:
                        return {"error": str(e), "status_code": 500}
                    except Exception as error:
                        return {"error": str(error)}

    async def radius_accounts(self, cmd='', site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/account" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/account" % site

            url = f"{self.base_url}{url_string}"

        match cmd.strip():
            case 'e':
                payload = {'': ''}

                async with self.ubiquipy_client_session as session:
                    try:
                        headers={
                                'Content-Type':'application/json',
                                'Cookie':self.token
                        }
                            
                        async with session.put(url=url, headers=headers, json=payload) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    except aiohttp.ClientError as e:
                        return {"error": str(e), "status_code": 500}
                    except Exception as error:
                        return {"error": str(error)}
                       
            case 'p':
                payload = {'': ''}
                    

                async with self.ubiquipy_client_session as session:
                    try:
                        headers={
                                'Content-Type':'application/json',
                                'Cookie':self.token
                        }
                            
                        async with session.post(url=url, headers=headers, json=payload) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    except aiohttp.ClientError as e:
                        return {"error": str(e), "status_code": 500}
                    except Exception as error:
                        return {"error": str(error)}


                       
            case 'g':
                async with self.ubiquipy_client_session as session:
                    try:
                        headers={
                            'Cookie':self.token
                        } 
                        async with session.get(url=url, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                nested_data = data['data']
                                response.close()
                                return nested_data
                            else:
                                return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                    except aiohttp.ClientError as e:
                        return {"error": str(e), "status_code": 500}
                    except Exception as error:
                        return {"error": str(error)}

    async def port_forwards(self, site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/portforward" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/portforward" % site

            url = f"{self.base_url}{url_string}"

        async with self.ubiquipy_client_session as session:
            try:
                headers={
                            'Cookie':self.token
                } 
                async with session.get(url=url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}
            except Exception as error:
                return {"error": str(error)}

    async def reports(self, interval='5', type='site', returned_data='bytes', macs=[], site='' ):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/report/%s.%s" % (site, interval, type)

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/report/%s.%s" % (site, interval, type)

            url = f"{self.base_url}{url_string}"
       
        if macs != []:
            payload = {'macs': macs}

            async with self.ubiquipy_client_session as session:
                try:
                    headers={
                                'Content-Type':'application/json',
                                'Cookie':self.token
                    }
                    async with session.post(url=url, headers=headers, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            nested_data = data['data']
                            response.close()
                            return nested_data
                        else:
                            return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                except aiohttp.ClientError as e:
                    return {"error": str(e), "status_code": 500}
                except Exception as error:
                    return {"error": str(error)}       

        else:
            async with self.ubiquipy_client_session as session:
                try:
                    headers={
                                'Cookie':self.token
                    }
                    async with session.post(url=url, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            nested_data = data['data']
                            response.close()
                            return nested_data
                        else:
                            return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
                except aiohttp.ClientError as e:
                    return {"error": str(e), "status_code": 500}
                except Exception as error:
                    return {"error": str(error)}

    async def auth_audit(self, start='', end='', site=''):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/authorization/" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/authorization/" % site

            url = f"{self.base_url}{url_string}"

        payload = {'start': start, 'end': end}

        async with self.ubiquipy_client_session as session:
            try:
                headers={
                    'Content-Type':'application/json',
                    'Cookie':self.token
                }
                async with session.post(url=url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                    return {"error": str(e), "status_code": 500}
            except Exception as error:
                    return {"error": str(error)} 

    async def mgr_sites(self, **kwargs):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/default/cmd/sitemgr/"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/default/cmd/sitemgr/" 

            url = f"{self.base_url}{url_string}"

        match str(kwargs.get('cmd')).strip():
                case 'g':
                    payload = {'cmd': 'get-admins'}

                case 'a':
                    payload = {'cmd': 'add-site', 'name': str(kwargs.get('name')), 'desc': str(kwargs.get('desc'))}
                
                case 'u':
                    payload = {'cmd': 'update-site',
                                      'name': kwargs.get('name'),
                                      'desc': kwargs.get('desc')}
                    
                case 'r':
                    payload = {'cmd': 'delete-site',
                                      'name': kwargs.get('name')}
                    
                case 'm':
                    payload = {'cmd': 'move-device',
                                      'mac': str(kwargs.get('mac')),
                                      'site_id': str(kwargs.get('site_id'))}
                    
                case 'd':
                    payload = {'cmd': 'delete-device',
                                      'mac': str(kwargs.get('mac'))}
                        
        async with self.ubiquipy_client_session as session:
            try:
                headers={
                    'Content-Type':'application/json',
                    'Cookie':self.token
                }
                async with session.post(url=url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                    return {"error": str(e), "status_code": 500}
            except Exception as error:
                    return {"error": str(error)} 

    async def mgr_clients(self, **kwargs):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/default/cmd/stamgr/"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/default/cmd/stamgr/" 

            url = f"{self.base_url}{url_string}"

        match str(kwargs.get('cmd')).strip():
            case 'b':
                payload = {'cmd': 'block-sta',
                                      'mac': kwargs.get('mac')}
                    
            case 'k':
                payload = {'cmd': 'kick-sta',
                                      'mac': kwargs.get('mac')}
                    
            case 'u':
                payload = {'cmd': 'unblock-sta',
                                      'mac': kwargs.get('mac')}
                    
            case 'f':
                payload = {'cmd': 'forget-sta',
                                      'mac': kwargs.get('mac')}
                    
            case 'r':
                payload = {'cmd': 'unauthorize-guest',
                                      'mac': kwargs.get('mac')}

        async with self.ubiquipy_client_session as session:
            try:
                headers={
                    'Content-Type':'application/json',
                    'Cookie':self.token
                }
                async with session.post(url=url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                    return {"error": str(e), "status_code": 500}
            except Exception as error:
                    return {"error": str(error)} 

    async def mgr_devices(self, **kwargs):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/default/cmd/stamgr/"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/default/cmd/stamgr/" 

            url = f"{self.base_url}{url_string}"

        match str(kwargs.get('cmd')).strip():
                case 'a':
                    payload = {'cmd': 'adopt',
                                      'mac': kwargs.get('mac')}
                    
                case 'r':
                    payload = {'cmd': 'restart',
                                      'mac': kwargs.get('mac')}
                    
                case 'f':
                    payload = {'cmd': 'force-provision',
                                      'mac': kwargs.get('mac')}
                    
                case 'p':
                    payload = {'cmd': 'power-cycle',
                                      'mac': kwargs.get('mac'),
                                      'port_idx': kwargs.get('port_idx')}
                    
                case 's':
                    payload = {'cmd': 'speedtest',
                                      'mac': kwargs.get('mac')}
                case 'S':
                    payload = {'cmd': 'speedtest-status',
                                      'mac': kwargs.get('mac')}
                case 'l':
                    payload = {'cmd': 'set-locate',
                                      'mac': kwargs.get('mac')}
                case 'L':
                    payload = {'cmd': 'unset-locate',
                                      'mac': kwargs.get('mac')}
                case 'u':
                    payload = {'cmd': 'upgrade',
                                      'mac': kwargs.get('mac')}
                case 'U':
                    
                    if url.strip() == '':
                        print('Enter the URL for the firmware to update to.')
                    else:
                        print('Updating...')
                        payload = {'cmd': 'upgrade-external',
                                        'mac': kwargs.get('mac'),
                                        'url': kwargs.get('url')}
                case 'm':
                    if self.inform_url.strip() == '':
                        print('Enter the new inform URL to migrate the device: %s to.' % kwargs.get('mac'))
                    else:
                        ('Migrating...')
                        payload = {'cmd': 'migrate',
                                        'mac': kwargs.get('mac'),
                                        'inform_url': self.inform_url}
                case 'M':
                    payload = {'cmd': 'cancel-migrate',
                                      'mac': kwargs.get('mac')}
                case 'w':
                    payload = {'cmd': 'spectrum-scan',
                                      'mac': kwargs.get('mac')}

        async with self.ubiquipy_client_session as session:
            try:
                headers={
                    'Content-Type':'application/json',
                    'Cookie':self.token
                }
                async with session.post(url=url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        nested_data = data['data']
                        response.close()
                        return nested_data
                    else:
                        return {"message": "Site DPI stat retrieval failed", "status_code": response.status}
            except aiohttp.ClientError as e:
                    return {"error": str(e), "status_code": 500}
            except Exception as error:
                    return {"error": str(error)} 

    