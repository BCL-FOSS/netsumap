from quart import Quart
import nest_asyncio
import os
from models.util.RedisDB import RedisDB


# Create folder for uploaded PCAP CSVs 
if os.path.isdir(os.path.join(os.path.dirname(__file__), 'Uploads')) is False:
    os.makedirs(os.path.join(os.path.dirname(__file__), 'Uploads'))
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Uploads'))
    print("CSV directory created successfully", flush=True)
else:
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Uploads'))
    print("CSV directory already created", flush=True)

# Initialize Quart App
app = Quart(__name__)
app.config.from_object("config")

app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADER'] = 'application/json'

# Connect to Redis DB
app.config['DB_CONN'] = RedisDB(hostname=app.config['REDIS_DB'], port=app.config['REDIS_DB_PORT'])

if app.config['DB_CONN'] is None:
    print('Verify Redis DB is installed and/or running. Ctrl + C to close netsumap', flush=True) 
    exit()
else:
    print("Redis DB Connected", flush=True)

nest_asyncio.apply()





    
