from quart import Quart, request
import json
import asyncio
from models.broker import Broker
from init_app import app
import websocket
from websocket import create_connection

websocket.enableTrace = True
ws=create_connection("ws://45.63.53.182:30000/ws")

@app.post("/unifi_webhook")
async def webhook():
    try:
        data = await request.get_json()
        if data:
            msg = json.dumps(data)
            unifi_event = {
                "uid":"",
                "type": "",
                "message": msg,
            }
            await ws.send(unifi_event)
        else:
            raise Exception('Ensure JSON message is attached to the request')
    except Exception as e:
        return {'Error' : e}
    finally:
        return {'Success' : 'Check the websocket UI'}


def run() -> None:
    app.run()





