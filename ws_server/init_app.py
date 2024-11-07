from quart import Quart

app = Quart(__name__)
app.secret_key = app.config['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config.from_object("config")