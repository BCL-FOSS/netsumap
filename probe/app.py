from flask import jsonify, request
from init_app import app
import uuid
import iperf3
import sqlite3
from sqlite3 import Connection

main_network = app.config['NETWORK_OBJ']

db_path = app.config['PROBE_DB_PATH']

@app.route('/pcap', methods=['POST'])
def pcap():
    scan_options = request.get_json(silent=True)
    if scan_options:
        pcap_dir = str(app.config['PCAP_FOLDER'])
        pcap_id = uuid.uuid4
        pcap_file = pcap_dir+str(pcap_id)+"pcap.pcap"
        main_network.pcap_scan(iface=scan_options['iface'], count=scan_options['count'], pcap_path=pcap_file)

@app.route('/bdwthtst' , methods=['POST'])
def bdwthtst():

    db_conn = sqlite3.connect(db_path)

    if isinstance(db_conn, Connection):
        app.config['USE_DB'] = True
        print(db_conn, flush=True)

    cur = db_conn.cursor()
    core_url_search = cur.execute("SELECT core_url FROM pbdata")
    core_url = core_url_search.fetchone()
    print(core_url, flush=True)
    iperf_url = str(core_url)+"/iperf"
    print(iperf_url, flush=True)
    port = app.config['IPERF_PORT']

    client = iperf3.Client()
    client.server_hostname = iperf_url
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

    db_conn.close()
    return response_data

@app.route('/allsrvcs' , methods=['GET'])
def allsrvcs():
    process_names_to_filter = ["python", "bash", "nginx"]  # Replace with desired process names
    filtered_processes = main_network.get_processes_by_names(process_names=process_names_to_filter)
    
    if filtered_processes:
        print(f"Processes matching {process_names_to_filter}:", flush=True)
        for process in filtered_processes:
            print(f"PID: {process['pid']}, Name: {process['name']}, Cmdline: {process['cmdline']}", flush=True)
    else:
        print(f"No processes found matching {process_names_to_filter}.", flush=True)
        
@app.errorhandler(404)
def page_not_found():
    return jsonify({"error": "Resource not found or does not exist"}), 404

@app.errorhandler(500)
def handle_internal_error(e):
    print(e, flush=True)
    return jsonify({"error": "Internal server error"}), 500

def run() -> None:
    app.run()



