from quart import render_template
from init_app import app

# export SECRET_KEY=secrets.token_urlsafe(16)
app.secret_key = app.config['SECRET_KEY']

@app.get("/")
async def index():
    return await render_template("index.html")

@app.get("/about_netifidash")
async def about():
    return await render_template("about_netifidash")