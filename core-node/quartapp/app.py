from quart import request, render_template, jsonify, flash, request, redirect, url_for
import json
from init_app import app
from models.util.CoreNetwork import Network
import numpy as np
import asyncio
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from sklearn.preprocessing import StandardScaler
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
from pathlib import Path
import uuid
import iperf3
from iperf3 import TestResult
import aiohttp
from models.util.NN import NN

# init Redis DB connection
db = app.config['DB_CONN']
aiopost = aiohttp.ClientSession()

K.clear_session() # Clears GPU resources before loading model

ALLOWED_EXTENSIONS = {'csv'}

# Load model defined in config file

# model = load_model(app.config['MODEL'])  

@app.route('/favicon.ico')
async def favicon():
    return '', 204

@app.errorhandler(404)
async def page_not_found():
    return await render_template("404.html")

@app.errorhandler(500)
async def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

@app.get("/")
async def index():
    return await render_template("index.html")

@app.get("/dashboard")
async def dash():
    return await render_template("dashboard.html", test_func=test_func)

@app.get("/probemgr")
async def probe_mgr():
    return await render_template("probemgr.html")

@app.get("/assets")
async def assets():
    return await render_template("blank.html")

@app.get("/netmap")
async def net_map():
    return await render_template("net_map.html")

@app.get("/netscan")
async def net_scan():
    return await render_template("blank.html")

@app.get("/uptime")
async def uptime():
    return await render_template("blank.html")

@app.get("/performance")
async def net_perf():
    return await render_template("blank.html")

@app.get("/inference")
async def inference():
    return await render_template("inference.html")

@app.route('/upload_csv', methods=['POST'])
async def upload_csv():
    try:
        file = (await request.files)['file']
        
        if file:
            print('CSV file attached', flush=True)
        else:
            return f"CSV not in payload", 0
            
        filename = secure_filename(file.filename)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        await file.save(file_path)

        return jsonify({"message": f"{filename} uploaded successfully!"})
    except Exception as e:
         return jsonify({
            'status': 'error',
            'message': str(e)
        })
    

@app.route("/csv_inference")
async def csv_inference():
    try:
        path = request.args.get('f_path', '')
        name = request.args.get('f_name', '')
        print(f"File Name: {name}\nFile Path: {path}", flush=True)

        payload = {'file_name': name,
                'file_path': path}
        
        """
            X_inference, original_data = preprocess_file_for_inference(file_path=path)
                        
            inference_value = predict(processed_input=X_inference)
        """
        return payload
    except Exception as e:
         return {
            'status': 'error',
            'message': str(e)
        }

@app.post("/json_inference")
async def rest_prediction():
    ml_obj = NN()
    try:
        if request.method == 'POST':
        
            data_value = await request.get_json()

            if data_value['packet_data']:

                json_data = dict(data_value)

                # JSON preprocessing for prediction
                X_input = ml_obj.preprocess_input(json_data=data_value['packet_data'])

                # Response conversion to JSON
                prediction = ml_obj.predict(processed_input=X_input)
                inference_value = json.dumps(prediction)
            else:
                return jsonify({"Error": "Packet data missing for threat assessment"})

            K.clear_session()

            return {
                "status": "success",
                "predictions": inference_value
            }
        else:
            return 0
    
    except Exception as e:
         return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    
@app.post("/enroll")
async def probe_registration():
    try:
        await db.ping_db()
        data_value = await request.get_json()
        if data_value:
            print(data_value, flush=True)

            # Extract specific fields from the JSON data
            probe_id = data_value["id"]
            probe_ip = data_value["ip"]
            host_name = data_value["hst_nm"]
            ports = data_value["ports"]
            ifaces = data_value["ifaces"]

            # Example debug output of extracted values
            print(f"Probe ID: {probe_id}", flush=True)
            print(f"Probe Data: {probe_ip}", flush=True)
            print(f"Host Name: {host_name}", flush=True)
            print(f"Ports: {ports}", flush=True)
            print(f"Interfaces: {ifaces}", flush=True)

            db_upload = await db.upload_db_data(id=probe_id, data=data_value)
            
            print(db_upload, flush=True)
        
            db_query_value = await db.get_obj_data(key=probe_id)
            print(db_query_value, flush=True)

            return {
                "id": probe_id,
                "probe_data": probe_ip,
                "host_name": host_name,
                "ports": ports,
                "ifaces": ifaces
            }
            
    except Exception as e:
         return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    
@app.post("/unenroll")    
async def probe_removal():
    try:
        data_value = await request.get_json()
        if data_value:
            probe_to_rm = json.dumps(data_value)

            if probe_to_rm['confirm'] == 'y':
                print(probe_to_rm['id'])

            return probe_to_rm #status
        else:
            return 0
    except Exception as e:
         return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    
@app.post("/pong")
async def pong():
    try:
        data = await request.get_json()
        if data:
            msg = json.dumps(data)

            evt_data = json.loads(msg)

            print(evt_data)

        else:
            raise Exception('Ensure JSON message is attached to the request')
    except Exception as e:
         return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    
@app.route("/check_uptime")
async def check_uptime():
    try:
        host_check = Network()
        id = request.args.get('id')
        ip = request.args.get('ip')
        hostname = request.args.get('hostname') 
        ports = request.args.get('ports') 

        ports_to_scan = [int(n) for n in ports[1:-1].split(",")]

        if ports_to_scan:
            for port in ports_to_scan:
                print(port, flush=True)

            ans, unans = host_check.check_service(ip=ip, host_name=hostname, port_list=ports_to_scan)

            if ans and unans:
                print(json.dumps({
                    'ans_pckts': ans.summary(),
                    'unans_pckts': unans.summary()
                }), flush=True)
                
                return json.dumps({
                    'ans_pckts': ans.summary(),
                    'unans_pckts': unans.summary()
                })
        else:
            return json.dumps({
                    'error': 'no ports selected. ICMP is not available.'
                })
    except Exception as e:
         return json.dumps({
            'status': 'error',
            'message': str(e)
        })
    
@app.route("/run_pcap")
async def run_pcap():
    try:
        
        ifaces = request.args.get('ifaces') 

        ifaces_to_scan = [n for n in ifaces[1:-1].split(",")]

        if ifaces_to_scan:
            for iface in ifaces_to_scan:
                print(iface, flush=True)

        else:
            return json.dumps({
                    'error': 'no interface(s) selected.'
                })
    except Exception as e:
         return json.dumps({
            'status': 'error',
            'message': str(e)
        })
    

    
@app.route('/all_probes')
async def all_probes():
    try:
        await db.ping_db()
        match = "prb*"
        db_query_value = await db.get_all_data(match=match)

        if db_query_value:
            print(json.dumps(db_query_value), flush=True)
        else:
            return {
            'status': 'error',
            'message': 'no probes have been adopted to this netsumap-core'
        }

        # Return JSON response
        return db_query_value
    except Exception as e:
         return {
            'status': 'error',
            'message': str(e)
        }

@app.route('/all_pcaps')
async def all_pcaps():
    try:
        csv_dir_path = app.config['UPLOAD_FOLDER']

        pcap_list={}

        main_path = Path(csv_dir_path).rglob('*.csv')
        if main_path:
            for file_path in main_path:
                file_name = file_path.name
                path = str(file_path.absolute().resolve())
                pcap_obj = {
                    "file_name": file_name,
                    "file_path": path, 
                }

                pcap_list[file_name] = pcap_obj
        else:
            return {
            'status': 'error',
            'message': 'no pcap csvs found. please upload your own files or set the probe in capture mode.'
        } 

        # Return JSON response
        return pcap_list
    except Exception as e:
         return jsonify({
            'status': 'error',
            'message': str(e)
        })
    
@app.route("/speed_test")
async def speed_test():
    try:
        hostname = request.args.get('hostname') 
        
        ports = request.args.get('ports') 

        port_to_scan = [int(n) for n in ports[1:-1].split(",") if int(n) == 5000]

        if port_to_scan:
            for port in port_to_scan:
                if port == 5000:
                    print(port, flush=True)
                    url = hostname+f":{port}"+"/bdwthtst"

        payload = {"": ""}

        async with aiopost as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    response_data = await response.json()
                    return response_data, 200
                else:
                    error_message = await response.text()
                    return {"error": error_message}, response.status
            
    except Exception as e:
         return json.dumps({
            'status': 'error',
            'message': str(e)
        })

@app.route('/background_process_test')
async def background_process_test():
    print ("Hello", flush=True)
    return {"status": "From background process"}

@app.route('/background_input_test')
def background_input_test():
    # Get values from the request arguments
    user_input = request.args.get('user_input', '')  
    print("User Input:", user_input, flush=True)
    # You can add more logic here to process the input
    return jsonify(result=f"Processed input: {user_input}")

def gen_id():
    id = uuid.uuid4()
    if id:
        return str(id)
    else:
        return 0   
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def test_func():
    return "from quart"