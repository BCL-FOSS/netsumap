from quart import Quart
import nest_asyncio

app = Quart(__name__)
app.secret_key = app.config['SECRET_KEY']
app.config.from_object("config")
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
nest_asyncio.apply()
    
