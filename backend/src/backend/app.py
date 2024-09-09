from quart import request
import json
from init_app import app
import websocket
from websocket import create_connection
from models.UniFiNetAPI import UniFiNetAPI
from models.util_models.PDF import PDF
from models.util_models.Utility import Utility
import asyncio

@app.post("/unifi_auth")
async def ubnt_auth():
    try:

        loop = asyncio.new_event_loop()
        auth_loop = asyncio.new_event_loop()
        
        data_value = loop.run_until_complete(request.get_json())

        if data_value:
            print('Data coroutine complete')
            json_data = json.dumps(data_value)
            data = json.loads(json_data)
            
            print(data)

        ubnt_profile = UniFiNetAPI(controller_ip=data['ip'], controller_port=data['port'], username=data['username'], password=data['password'])
        

        profile_value = auth_loop.run_until_complete(ubnt_profile.authenticate())


        loop.close()
        auth_loop.close()
        return profile_value

        #def sync_processor():
        #    unifi_profile = generate_ubiquipy_profile(ip=str(dump['ip']), port=str(dump['port']), user_name=str(dump['username']), pass_word=str(dump['password']))
        #    return unifi_profile

        #task_result = loop.create_task(sync_processor())
        #result_value = loop.run_until_complete(task_result)

        #if task_result.done():
        #    print('Result coroutine complete')
        #    print(jsonify(result_value))

    except TypeError as error:
        return {'TypeError' :  str(error)}
    except Exception as e:
        return {'Exception' :  str(e)}
    

@app.post("/unifi_webhook")
async def webhook():
    try:
        data = await request.get_json()
        if data:
            data = json.dumps(data)
            #unifi_event = {
            #    "message": str(data)
            #}
            ws = activate_websocket()
            await ws.send(str(data))
        else:
            raise Exception('Ensure JSON message is attached to the request')
    except Exception as e:
        return {'Error' : e}
    finally:
        return {'try_catch_end' : 'Check the frontend UI'}
    
def generate_ubiquipy_profile(ip='', port='', user_name='', pass_word=''):
    try:
        ubnt_profile = UniFiNetAPI(controller_ip=ip, controller_port=port, username=user_name, password=pass_word)
        result = ubnt_profile.authenticate()
        return result
    except Exception as e:
        return {'Error' : e}

def activate_websocket():
    websocket.enableTrace = True
    ws=create_connection(app.config['WEBSOCKET_ADDRESS'])
    return ws

def run() -> None:
    try:

        app.run()

    except OSError as oserror:
        return{"Application Server Error": "Server is already running. Please stop and restart the service.\n" + str(oserror)}