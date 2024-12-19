from flask import jsonify, request
from init_app import app
import requests
import os
import uuid
import iperf3
from iperf3 import TestResult

main_network = app.config['NETWORK_OBJ']

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
    test_options = request.get_json(silent=True)
    hostname = test_options['hostname']
    port_to_scan = test_options['port']
    client = iperf3.Client()
    client.server_hostname = hostname
    client.port = port_to_scan
    client.json_output = True
    client.reverse = True
        
    result = client.run()

    if isinstance(result, TestResult):
        print(result, flush=True)

    if result.error:
        print(result.error, flush=True)
    else:
        print('', flush=True)
        print('Test completed:', flush=True)
        print('  started at         {0}'.format(result.time), flush=True)
        print('  bytes transmitted  {0}'.format(result.bytes), flush=True)
        print('  jitter (ms)        {0}'.format(result.jitter_ms), flush=True)
        print('  avg cpu load       {0}%\n'.format(result.local_cpu_total), flush=True)

        print('Average transmitted data in all sorts of networky formats:', flush=True)
        print('  bits per second      (bps)   {0}'.format(result.bps), flush=True)
        print('  Kilobits per second  (kbps)  {0}'.format(result.kbps), flush=True)
        print('  Megabits per second  (Mbps)  {0}'.format(result.Mbps), flush=True)
        print('  KiloBytes per second (kB/s)  {0}'.format(result.kB_s), flush=True)
        print('  MegaBytes per second (MB/s)  {0}'.format(result.MB_s), flush=True)

    return result
        
@app.errorhandler(404)
def page_not_found():
    return jsonify({"error": "Resource not found or does not exist"}), 404

@app.errorhandler(500)
def handle_internal_error(e):
    print(e, flush=True)
    return jsonify({"error": "Internal server error"}), 500

def run() -> None:
    app.run()



