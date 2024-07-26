from quart import render_template, websocket, request, redirect, url_for
import asyncio
from models.broker import Broker
from init_app import app
from quart_auth import QuartAuth, login_required, AuthUser, login_user, current_user, logout_user
import os
from secrets import compare_digest

broker = Broker()

# export SECRET_KEY=secrets.token_urlsafe(16)
app.secret_key = app.config['SECRET_KEY']

QuartAuth(app)


async def _receive() -> None:
    while True:
        message = await websocket.receive()
        await broker.publish(message)


@app.get("/")
@login_required
async def index():
    print(f"{current_user.auth_id} has signed in")
    return await render_template("index.html")

@app.get("/about_netifidash")
async def about():
    return await render_template("about_netifidash")

@app.route("/login", methods={"GET","POST"})
async def login():
    if request.method == 'POST':
        data = await request.json()
        if data["username"] == app.config['GUI_USER'] and compare_digest(data["password"], app.config['GUI_PASSWORD']):
            login_user(AuthUser(app.config['GUI_USER']))
            return redirect(url_for("index"))
        else:
            return redirect(url_for("about"))
    return """

    <form method ="POST">
    <input name="username">
    <input name="password" type="password">
    <input type="submit" value="Login">
    </form>

    """

@app.route("/logout")
async def logout():
    logout_user()
    return redirect(url_for("about"))

@app.websocket("/ws")
async def ws() -> None:
    try:
        task = asyncio.ensure_future(_receive())
        async for message in broker.subscribe():
            await websocket.send(message)
    except Exception as e:
        await websocket.accept()
        await websocket.close(1000)
        raise e
        print()
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