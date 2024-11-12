from quart import render_template, jsonify
from init_app import app

@app.get("/")
async def app_main():
    return await render_template("index.html")

@app.errorhandler(404)
async def page_not_found():
    return await render_template("404.html")

@app.errorhandler(500)
async def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

def run() -> None:
    app.run()


    