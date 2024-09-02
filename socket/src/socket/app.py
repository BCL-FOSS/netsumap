from quart import websocket
import asyncio
from models.broker import Broker
from init_app import app

broker = Broker()

# export SECRET_KEY=secrets.token_urlsafe(16)
app.secret_key = app.config['SECRET_KEY']


async def _receive() -> None:
    while True:
        message = await websocket.receive()
        await broker.publish(message)

@app.websocket("/")
async def ws() -> None:
    try:
        task = asyncio.ensure_future(_receive())
        async for message in broker.subscribe():
            await websocket.send(message)
    except Exception as e:
        await websocket.accept()
        await websocket.close(1000)
        raise e
    except asyncio.CancelledError:
        # Handle disconnection here
        await websocket.accept()
        await websocket.close(1000)
        raise Exception(asyncio.CancelledError)
    finally:
        task.cancel()
        await task
        await websocket.accept()
        await websocket.close(1000)

def run() -> None:
    app.run()