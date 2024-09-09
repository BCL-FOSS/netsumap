from quart import request, jsonify
import json
from init_app import app
import websocket
from websocket import create_connection
import os
from models.UniFiNetAPI import UniFiNetAPI
from models.util_models.PDF import PDF
from models.util_models.Utility import Utility
import asyncio
import time
import nest_asyncio
from concurrent.futures import ThreadPoolExecutor
from ast import literal_eval


_executor = ThreadPoolExecutor(1)


@app.post("/unifi_auth")
async def ubnt_auth():
    try:

        nest_asyncio.apply()
        loop = asyncio.new_event_loop()
        
        data_value = loop.run_until_complete(request.get_data())

        if data_value:
            data = literal_eval(data_value)
            print('Data coroutine complete')

            json_data = json.dumps(data, indent=4, sort_keys=True)

            print(json_data)

        loop.close()

        #def sync_processor():
        #    unifi_profile = generate_ubiquipy_profile(ip=str(dump['ip']), port=str(dump['port']), user_name=str(dump['username']), pass_word=str(dump['password']))
        #    return unifi_profile

        #task_result = loop.create_task(sync_processor())
        #result_value = loop.run_until_complete(task_result)

        #if task_result.done():
        #    print('Result coroutine complete')
        #    print(jsonify(result_value))

    except TypeError as error:
        if " The response value returned by the view function cannot be None" in error:
            pass
        else:
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
    app.run()