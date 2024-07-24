import asyncio
from quart import websocket
from models.broker import Broker
import aioredis
from init_app import app

broker = Broker()

async def _receive() -> None:
    while True:
        message = await websocket.receive()
        await broker.publish(message)

async def add_session():
    redis = await aioredis.from_url("redis://localhost", username="user", password="sEcRet")
    await redis.set("my-key", "value")
    value = await redis.get("my-key")
    print(value)

@app.websocket("/ws")
async def ws() -> None:
    try:
        task = asyncio.ensure_future(_receive())
        async for message in broker.subscribe():
            await websocket.send(message)
    finally:
        task.cancel()
        await task