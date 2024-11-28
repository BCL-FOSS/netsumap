from flask import Flask
import os
from models.RedisDB import RedisDB
from models.NetsumapCoreConn import NetsumapCoreConn
from models.ProbeNetwork import ProbeNetwork
from models.Probe import Probe
import aiohttp


app = Flask(__name__)
app.config.from_object("config")

folder_name = 'probe_data'
data_dir_path = os.path.join(app.instance_path, folder_name)

# Create probe data folder 
if os.path.isdir(data_dir_path) is False:
    os.makedirs(data_dir_path, exist_ok=True)
    print(f"Probe data directory {data_dir_path} created successfully", flush=True)
else:
    pass

# General quart settings
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['PROBE_DATA_FOLDER'] = data_dir_path
app.config['CORS_HEADER'] = 'application/json'

app.config['DB_CONN'] = RedisDB(hostname=app.config['REDIS_DB'], port=app.config['REDIS_DB_PORT'])
    
if app.config['DB_CONN'] is None:
    print('Verify Redis DB is installed and/or running. Ctrl + C to close netsumap', flush=True) 
    exit()
else:
    print("Redis DB Connected", flush=True)

app.config['PROBE_OBJ'] = Probe()
app.config['NETWORK_OBJ'] = ProbeNetwork()
app.config['CORE_CONN'] = NetsumapCoreConn()
app.config['REST_SESSION'] = aiohttp.ClientSession()
