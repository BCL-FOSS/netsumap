from flask import jsonify, request
from init_app import app

main_network = app.config['NETWORK_OBJ']

@app.route('/pcap', methods=['POST'])
def pcap_init():
    scan_options = request.get_json(silent=True)
    if scan_options is not None:
        main_network.pcap_scan(iface=scan_options['iface'], count=scan_options['count'])

@app.errorhandler(404)
def page_not_found():
    return jsonify({"error": "Resource not found or does not exist"}), 404

@app.errorhandler(500)
def handle_internal_error(e):
    print(e, flush=True)
    return jsonify({"error": "Internal server error"}), 500

def run() -> None:
    app.run()

