from quart import render_template, jsonify
from init_app import app

# export SECRET_KEY=secrets.token_urlsafe(16)
app.secret_key = app.config['SECRET_KEY']

@app.get("/")
async def index():
    return await render_template("index.html")

@app.get("/app")
async def app_main():
    return await render_template("web_app.html")


@app.errorhandler(404)
async def page_not_found():
    return await render_template("404.html")

@app.errorhandler(500)
async def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500