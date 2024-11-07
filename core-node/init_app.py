from quart import Quart
import nest_asyncio
import os

if os.path.isdir(os.path.join(os.path.dirname(__file__), 'Uploads')) is False:
    os.makedirs(os.path.join(os.path.dirname(__file__), 'Uploads'))
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Uploads'))
else:
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Uploads'))

app = Quart(__name__)
app.secret_key = app.config['SECRET_KEY']
app.config.from_object("config")
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADER'] = 'application/json'
nest_asyncio.apply()
    
