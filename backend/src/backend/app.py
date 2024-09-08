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

@app.post("/unifi_auth")
async def ubnt_auth():
    try:
        my_tasks = set()
        dump = {}

        task_data = asyncio.create_task(request.get_json())
        my_tasks.add(task_data)
        task_data.add_done_callback(my_tasks.discard)

        if task_data.done():
            print('Data coroutine complete')
            dump = jsonify(task_data.result())

        def sync_processor():

            unifi_profile = generate_ubiquipy_profile(ip=str(dump.get_json()['ip']), port=str(dump.get_json()['port']), user_name=str(dump.get_json()['username']), pass_word=str(dump.get_json()['password']))
            return unifi_profile

        task_result = asyncio.create_task(sync_processor())
        my_tasks.add(task_result)
        task_result.add_done_callback(my_tasks.discard)

        if task_result.done():
            print('Result coroutine complete')
            result = jsonify(task_result.result())

        return result

    except TypeError as error:
        return {'Error' :  str(error)}
    

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
        id = ubnt_profile.authenticate()
    except Exception as e:
        return {'Error' : e}

    return id

def activate_websocket():
    websocket.enableTrace = True
    ws=create_connection(app.config['WEBSOCKET_ADDRESS'])
    return ws

def run() -> None:
    app.run()