from flask import jsonify, request
from init_app import app
import requests
import os
import uuid
import iperf3
from iperf3 import TestResult
import sqlite3
from sqlite3 import Connection
from pathlib import Path

main_network = app.config['NETWORK_OBJ']

db_search_path = os.getcwd()

db_path = Path(db_search_path).rglob('*.db')

db_conn = sqlite3.connect(db_path)

if isinstance(db_conn, Connection):
    app.config['USE_DB'] = True


@app.route('/pcap', methods=['POST'])
def pcap():
    scan_options = request.get_json(silent=True)
    if scan_options:
        pcap_dir = str(app.config['PCAP_FOLDER'])
        pcap_id = uuid.uuid4
        pcap_file = pcap_dir+str(pcap_id)+"pcap.pcap"
        main_network.pcap_scan(iface=scan_options['iface'], count=scan_options['count'], pcap_path=pcap_file)

@app.route('/test' ,methods=['POST'])
def test():

    cur = db_conn.cursor()
    core_url_search = cur.execute("SELECT url FROM pbdata")
    core_url = core_url_search.fetchone()
    print(core_url, flush=True)
    port = app.config['IPERF_PORT']

    client = iperf3.Client()
    client.server_hostname = str(core_url)
    client.port = port
    client.json_output = True
    client.reverse = True

    result = client.run()

    if result.error:
        return jsonify({"error": result.error}), 400

    response_data = {
        "start_time": result.time,
        "bytes_transmitted": result.bytes,
        "jitter_ms": result.jitter_ms,
        "local_cpu_total": result.local_cpu_total,
        "bps": result.bps,
        "kbps": result.kbps,
        "Mbps": result.Mbps,
        "kB_s": result.kB_s,
        "MB_s": result.MB_s
    }

    cur.close()

    return response_data
        
@app.errorhandler(404)
def page_not_found():
    return jsonify({"error": "Resource not found or does not exist"}), 404

@app.errorhandler(500)
def handle_internal_error(e):
    print(e, flush=True)
    return jsonify({"error": "Internal server error"}), 500

def run() -> None:
    app.run()



