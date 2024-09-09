from quart import Quart, websocket, request
import nest_asyncio

app = Quart(__name__)
app.secret_key = app.config['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config.from_object("config")
nest_asyncio.apply()