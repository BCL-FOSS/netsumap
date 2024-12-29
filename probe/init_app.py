from flask import Flask
import os
from config.models.Network import Network
import os
from pathlib import Path
import sqlite3
from sqlite3 import Connection

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

pcap_dir = 'pcaps'
pcap_save_path = os.path.join(data_dir_path, pcap_dir)

# Create pcap file folder 
if os.path.isdir(pcap_save_path) is False:
    os.makedirs(pcap_save_path, exist_ok=True)
    print(f"Probe pcap directory {pcap_save_path} created successfully", flush=True)
else:
    pass

# Locate probe database
db_search_path = os.getcwd()
db_search_result = Path(db_search_path).rglob('*.db')
if db_search_result:
    for file_path in db_search_result:
        db_path = str(file_path.absolute().resolve())
        print(db_path)
    db_search_result.close()
else:
    print('No probe database found. Verify initial probe enrollment completed successfully.')
    exit()

# General Probe Configurations
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['PROBE_DATA_FOLDER'] = data_dir_path
app.config['PCAP_FOLDER'] = pcap_save_path
app.config['PROBE_DB_PATH'] = db_path
app.config['CORS_HEADER'] = 'application/json'
app.config['NETWORK_OBJ'] = Network()



