from flask import jsonify, request
from init_app import app

db = app.config['DB_CONN']
main_network = app.config['NETWORK_OBJ']
probe = app.config['PROBE_OBJ']
core_conn = app.config['CORE_CONN']

@app.post("/pcap_init")
def pcap_init():
    scan_options = request.get_json(silent=True)
    if scan_options is not None:
        main_network.pcap_scan(iface=scan_options['iface'], count=scan_options['count'])

@app.errorhandler(404)
def page_not_found():
    return jsonify({"error": "Resource not found or does not exist"}), 404

@app.errorhandler(500)
def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

def run() -> None:
    app.run()