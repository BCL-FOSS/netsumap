from flask import Flask
import os
from models.RedisDB import RedisDB
from models.NetsumapCoreConn import NetsumapCoreConn
from models.Network import Network
from models.Probe import Probe
import threading
import iperf3
import os

def run_iperf_server():
    try:
    
        """Start the iPerf3 server on a separate thread."""
        server = iperf3.Server()
        main_network = Network()
        external_ip = main_network.get_public_ip()
        server.bind_address = external_ip
        iperf_port = int(os.getenv("IPERF_PORT"))
        server.port = iperf_port
        server.verbose = True 
        server.run()

    except Exception as e:
        print(e, flush=True)

    # print(f"Starting iPerf3 server on {external_ip}:{iperf_port}", flush=True)
    #    return None
    
    
def start_app():
    threading.Thread(target=run_iperf_server, daemon=True).start()

    return Flask(__name__)

app = start_app()

if app is None:
    print('Error occured during probe initialization. Verify iperf installation. ctrl+c to exit.', flush=True)
    exit()

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
    print('Verify Redis DB is installed and/or running. Ctrl + C to exit.', flush=True) 
    exit()
else:
    print("Redis DB Connected", flush=True)

app.config['PROBE_OBJ'] = Probe()
app.config['NETWORK_OBJ'] = Network()
app.config['CORE_CONN'] = NetsumapCoreConn()


