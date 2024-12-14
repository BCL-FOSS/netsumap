from flask import jsonify, request
from init_app import app
import requests
import os
import uuid

main_network = app.config['NETWORK_OBJ']

@app.route('/pcap', methods=['POST'])
def pcap_init():
    scan_options = request.get_json(silent=True)
    if scan_options:
        pcap_dir = str(app.config['PCAP_FOLDER'])
        pcap_id = uuid.uuid4
        pcap_file = pcap_dir+str(pcap_id)+"pcap.pcap"
        main_network.pcap_scan(iface=scan_options['iface'], count=scan_options['count'], pcap_path=pcap_file)

@app.errorhandler(404)
def page_not_found():
    return jsonify({"error": "Resource not found or does not exist"}), 404

@app.errorhandler(500)
def handle_internal_error(e):
    print(e, flush=True)
    return jsonify({"error": "Internal server error"}), 500

def run() -> None:
    app.run()



