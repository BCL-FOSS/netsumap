from quart import Quart
import asyncio
from models.broker import Broker
from init_app import app
import websocket
from websocket import create_connection

websocket.enableTrace = True
ws=create_connection("ws://45.63.53.182:30000/ws")

@app.post("/unifi_webhook")
async def webhook():
    ws.send("Message from backend. Backend -> Websocket")

def run() -> None:
    app.run()





