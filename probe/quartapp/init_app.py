from quart import Quart
import nest_asyncio
import sqlite3
import os

app = Quart(__name__)
app.config.from_object("config")

# Probe data folder settings
folder_name = 'probe_data'
data_dir_path = os.path.join(app.instance_path, folder_name)

if os.path.isdir(data_dir_path) is False:
    os.makedirs(data_dir_path, exist_ok=True)
    PROBE_DATA_FOLDER = data_dir_path
    print(f"Probe data directory {PROBE_DATA_FOLDER} created successfully", flush=True)
else:
    PROBE_DATA_FOLDER = data_dir_path

# General quart settings
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['PROBE_DATA_FOLDER'] = PROBE_DATA_FOLDER
app.config['CORS_HEADER'] = 'application/json'

# Probe DB settings
app.config['USE_DB'] = True
db_path = os.path.join(app.config['PROBE_DATA_FOLDER'], 'probe.db')
app.config['DB_PATH'] = db_path

if os.path.exists(app.config['DB_PATH']) == False:
    conn = sqlite3.connect(app.config['DB_PATH'])
    cur = conn.cursor()
    cur.execute("CREATE TABLE pbdata(id, status, host_ip, hostname)")
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is None:
        print('Failed to create table in db', flush=True)
        app.config['USE_DB']=False
else:
     print("Probe DB already exists", flush=True)
 
nest_asyncio.apply()