from quart import request
import json
from init_app import app
import websocket
from websocket import create_connection
import os

websocket.enableTrace = True
ws=create_connection(app.config['WEBSOCKET_ADDRESS'])

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

def run() -> None:
    app.run()





