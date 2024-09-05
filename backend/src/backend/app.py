from quart import request
import json
from init_app import app
import websocket
from websocket import create_connection
import os
from models.UniFiNetAPI import UniFiNetAPI
from models.util_models.PDF import PDF
from models.util_models.Utility import Utility

websocket.enableTrace = True
ws=create_connection(app.config['WEBSOCKET_ADDRESS'])

@app.post("/unifi_auth")
async def ubnt_auth():
    try:
        data = await request.get_json()
        if data:
            msg = json.dumps(data)
            return msg['username']
        
    except Exception as e:
        return {'Error' : e}

@app.post("/unifi_webhook")
async def webhook():
    try:
        data = await request.get_json()
        if data:
            msg = json.dumps(data)
            #unifi_event = {
            #    "message": str(msg)
            #}
            await ws.send(str(msg))
        else:
            raise Exception('Ensure JSON message is attached to the request')
    except Exception as e:
        return {'Error' : e}
    finally:
        return {'try_catch_end' : 'Check the frontend UI'}

def run() -> None:
    app.run()





