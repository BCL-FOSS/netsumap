from quart import Quart

from quart import request

from quart import jsonify

from quart_schema import QuartSchema, validate_request, validate_response


app = Quart(__name__)

def run() -> None:
    app.run()

@app.post("/echo")
async def echo():
    data = await request.get_json()
    return {"input": data, "extra": True}

@app.get("/example")
async def example():
    return jsonify(["a", "b"])