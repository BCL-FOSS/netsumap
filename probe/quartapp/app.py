from quart import request, render_template, jsonify, flash, redirect, url_for
import json
from init_app import app
from models.NetsumapCoreConn import NetsumapCoreConn
from models.ProbeNetwork import ProbeNetwork
import threading
import iperf3
import os
import sqlite3

folder_name = 'probe_data'
data_dir_path = os.path.join(app.instance_path, folder_name)
main_network = ProbeNetwork()
core_conn = NetsumapCoreConn()

@app.before_serving
async def start_iperf_server():
    """Ensure iPerf3 server starts when the app starts."""
    threading.Thread(target=run_iperf_server, daemon=True).start()

@app.before_serving
async def probe_data_dir():
    # Create probe data folder 
    if os.path.isdir(data_dir_path) is False:
        os.makedirs(data_dir_path, exist_ok=True)
        print(f"Probe data directory {data_dir_path} created successfully", flush=True)
    else:
        pass

@app.before_serving
async def register_probe():
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

@app.errorhandler(404)
async def page_not_found():
    return await render_template("404.html")

@app.errorhandler(500)
async def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

@app.post("/bdwthtest")
async def bandwidth_test():

    return None

def run_iperf_server():
    """Start the iPerf3 server on a separate thread."""
    server = iperf3.Server()
    external_ip = main_network.get_public_ip()
    server.bind_address = external_ip
    iperf_port = int(os.getenv("IPERF_PORT"))
    server.port = iperf_port
    server.verbose = True
    print(f"Starting iPerf3 server on {external_ip}:{iperf_port}", flush=True)
    server.run()

    if server == None:
        return {"error":"Failed to start iperf server. verify iperf installation"}

def run() -> None:
    app.run()