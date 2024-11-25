from quart import Quart
import nest_asyncio
import sqlite3
import os
from models.NetsumapCoreConn import NetsumapCoreConn
from models.ProbeNetwork import ProbeNetwork

app = Quart(__name__)
app.config.from_object("config")

main_network = ProbeNetwork()
core_conn = NetsumapCoreConn()

# Probe data folder settings
folder_name = 'probe_data'
data_dir_path = os.path.join(app.instance_path, folder_name)

# Create probe data folder 
if os.path.isdir(data_dir_path) is False:
    os.makedirs(data_dir_path, exist_ok=True)
    print(f"Probe data directory {data_dir_path} created successfully", flush=True)
else:
    pass

app.config['USE_DB'] = True
db_path = db_path = os.path.join(data_dir_path, 'probe.db')

if os.path.exists(db_path) == False:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE pbdata(id, status, host_ip, hostname)")
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is None:
        print('Failed to create table in db', flush=True)
        app.config['USE_DB']=False
else:
        print("Probe DB already exists", flush=True)
        
listening_ports = main_network.open_tcp_ports()
external_ip = main_network.get_public_ip()
core_conn.register(url=os.getenv("CORE_NAME"), public_ip=external_ip, USE_DB=app.config['USE_DB'],ports=listening_ports)

# General quart settings
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['PROBE_DATA_FOLDER'] = data_dir_path
app.config['CORS_HEADER'] = 'application/json'

nest_asyncio.apply()