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

nest_asyncio.apply()
loop = asyncio.new_event_loop()
_executor = ThreadPoolExecutor(1)


@app.post("/unifi_auth")
async def ubnt_auth():
    try:

        #task_data = loop.create_task(request.get_json())
        data_value = loop.run_until_complete(run_func_async(request.get_json))

        if data_value:
            print('Data coroutine complete')
            print(jsonify(data_value))

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
    
async def run_func_async(func=None):
    await loop.run_in_executor(_executor, func)
    
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