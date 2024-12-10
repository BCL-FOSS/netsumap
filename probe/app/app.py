from flask import jsonify, request
from init_app import app
import requests
import os

main_network = app.config['NETWORK_OBJ']

@app.route('/pcap', methods=['POST'])
def pcap_init():
    scan_options = request.get_json(silent=True)
    if scan_options is not None:
        main_network.pcap_scan(iface=scan_options['iface'], count=scan_options['count'], pcap_path=app.config['PCAP_FOLDER'])

@app.errorhandler(404)
def page_not_found():
    return jsonify({"error": "Resource not found or does not exist"}), 404

@app.errorhandler(500)
def handle_internal_error(e):
    print(e, flush=True)
    return jsonify({"error": "Internal server error"}), 500

def run() -> None:
    app.run()

def send_csv(url, csv_filepath):

    try:
        with open(csv_filepath, 'rb') as file:
            files = {'file': (csv_filepath, file, 'text/csv')}
          
            headers = {
                'Content-Type': 'text/csv'
            }
            response = requests.request("POST", url, headers=headers, files=files)

            if response.status_code == 200:
                print("Request successful.")
            else:
                print(f"Request failed with status code: {response.status_code}")

            return response.json()
    except FileNotFoundError:
        print(f"Error: The file {csv_filepath} does not exist.")
    except requests.RequestException as e:
        print(f"Error: Unable to send request to {url}. Details: {e}")

