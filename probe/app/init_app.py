from flask import Flask
import os
from models.Network import Network
import os

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

# General quart settings
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['PROBE_DATA_FOLDER'] = data_dir_path
app.config['PCAP_FOLDER'] = pcap_save_path
app.config['CORS_HEADER'] = 'application/json'

app.config['NETWORK_OBJ'] = Network()



