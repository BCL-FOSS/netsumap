from quart import Quart
import nest_asyncio
import os
import secrets
from models.util_models.RedisDB import RedisDB

if os.path.isdir(os.path.join(os.path.dirname(__file__), 'Uploads')) is False:
    os.makedirs(os.path.join(os.path.dirname(__file__), 'Uploads'))
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Uploads'))
else:
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Uploads'))

app = Quart(__name__)
app.config.from_object("config")

app.config['DB_CONN'] = RedisDB(hostname=app.config['REDIS_DB'], port=app.config['REDIS_DB_PORT'])

if app.config['DB_CONN'] is None:
    print('Verify Redis DB is installed and/or running. Ctrl + C to close netsumap', flush=True) 
    exit()
else:
    print("DB Connected", flush=True)

app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADER'] = 'application/json'
nest_asyncio.apply()

"""
if app.config['SECRET_KEY'] is None:
    app.config['SECRET_KEY'] = secrets.token_hex()

app.secret_key = app.config['SECRET_KEY']
login_manager = LoginManager()
login_manager.init_app(app)
app.config['LOGIN_MANAGER'] = login_manager

"""




    
