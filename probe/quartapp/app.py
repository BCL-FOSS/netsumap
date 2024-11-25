from quart import render_template, jsonify
from init_app import app
from models.NetsumapCoreConn import NetsumapCoreConn
from models.ProbeNetwork import ProbeNetwork
import threading
import iperf3
import os

folder_name = 'probe_data'
data_dir_path = os.path.join(app.instance_path, folder_name)
main_network = ProbeNetwork()

@app.before_serving
async def start_iperf_server():
    """Ensure iPerf3 server starts when the app starts."""
    threading.Thread(target=run_iperf_server, daemon=True).start()

@app.errorhandler(404)
async def page_not_found():
    return await render_template("404.html")

@app.errorhandler(500)
async def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

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