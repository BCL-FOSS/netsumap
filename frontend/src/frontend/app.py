from quart import render_template, request, redirect, url_for
from init_app import app
import websocket
from websocket import create_connection
import os
from quart_auth import login_required, AuthUser, login_user, current_user, logout_user, QuartAuth
import os
from secrets import compare_digest

# export SECRET_KEY=secrets.token_urlsafe(16)
app.secret_key = app.config['SECRET_KEY']

QuartAuth(app)

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
        data = await request.form
        if data["username"] == app.config['GUI_USER'] and compare_digest(data["password"], app.config['GUI_PASSWORD']):
            login_user(QuartAuth(app.config['GUI_USER']))
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