from quart import Quart
import asyncio
from models.broker import Broker
from init_app import app
import websocket
from websocket import create_connection


websocket.enableTrace = True
ws=create_connection("ws://gitxiv.com/sockjs/212/2aczpiim/websocket")

@app.post("/unifi_webhook")
async def webhook():
    ws.send()





