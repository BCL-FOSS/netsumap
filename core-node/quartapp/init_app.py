from quart import Quart
import nest_asyncio
import os
from models.util.RedisDB import RedisDB
import iperf3
import threading
from models.util.CoreNetwork import Network

def run_iperf_server():
    
    """Start the iPerf3 server on a separate thread."""
    server = iperf3.Server()
    main_network = Network()
    external_ip = main_network.get_public_ip()
    server.bind_address = external_ip
    iperf_port = 6363
    server.port = iperf_port
    server.verbose = True 

    while True:
        server.run()

def start_iperf():
    try:

        threading.Thread(target=run_iperf_server, daemon=True).start()

    except RuntimeError as error:
        print(f'error starting iperf server: {error}', flush=True)
        print('Error occured during probe initialization. Verify iperf installation. ctrl+c to exit.', flush=True)
        exit()

# Initialize Quart App
app = Quart(__name__)
app.config.from_object("config")

start_iperf()

folder_name = 'pcaps'
csv_dir_path = os.path.join(app.instance_path, folder_name)

# Create folder for uploaded PCAP CSVs
if os.path.isdir(csv_dir_path) is False:
    os.makedirs(csv_dir_path, exist_ok=True)
    UPLOAD_FOLDER = csv_dir_path
    print(f"CSV directory {UPLOAD_FOLDER} created successfully", flush=True)
else:
    UPLOAD_FOLDER = csv_dir_path

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





    
