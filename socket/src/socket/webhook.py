from quart import websocket, request
import asyncio
from init_app import app
import json
import websocket
from websocket import create_connection

@app.post("/ubnt_webhook")
async def webhook():
    try:
        data = await request.get_json()
        if data:
            data = json.dumps(data)
            #unifi_event = {
            #    "message": str(data)
            #}
            ws = activate_websocket_connection()
            await ws.send(str(data))
        else:
            raise Exception('Ensure JSON message is attached to the request')
    except Exception as e:
        return {'Error' : e}
    finally:
        return {'try_catch_end' : 'Check the frontend UI'}
    
def activate_websocket_connection():
    try:
        websocket.enableTrace = True
        ws=create_connection(app.config['WEBSOCKET_ADDRESS'])
        return ws
    except Exception as e:
        return {"Websocket Connection Error" : "Please verify the websocket server is online and accessible",
                "Error Message" : str(e)}