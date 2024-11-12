from quart import request, render_template, jsonify
import json
from init_app import app
from models.UniFiNetAPI import UniFiNetAPI
from models.util_models.RedisDB import RedisDB
from models.util_models.Uptime import Uptime
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
from ast import literal_eval

# init Redis DB connection
db = RedisDB(hostname=app.config['REDIS_DB'], port=app.config['REDIS_DB_PORT']) 

if db is None:
    print('Verify Redis DB is installed and/or running. Ctrl + C to close the program', flush=True) 
    exit()
else:
    print("DB Connected", flush=True)

K.clear_session() # Clears GPU resources before loading model

# Allowed files extensions for /file_analysis 
ALLOWED_EXTENSIONS = set(['csv'])

# Load model defined in config file

# model = load_model(app.config['MODEL'])  

@app.errorhandler(404)
async def page_not_found():
    return await render_template("404.html")

@app.errorhandler(500)
async def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

@app.get("/")
async def index():
    return await render_template("index.html")

@app.post("/csv_inference")
async def file_prediction():
    try:
        if request.method == 'POST':
            file = request.files.getlist('files')
            filename = ""
            analysis_results = []
            for f in file:
                if 'csv_file' not in f:
                    return jsonify({"error": "No file part in the request"}), 400
                
                #print(f.filename)
                filename = secure_filename(f.filename)
                #print(allowedFile(filename))
                if allowedFile(filename):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    f.save(file_path)
                    X_inference, original_data = preprocess_file_for_inference(file_path=file_path)
                    
                    inference_value = predict(processed_input=X_inference)

                    analysis_results.append(inference_value)

                else:
                    return jsonify({'message': 'File type not allowed'}), 400
                
            inference_values = json.dumps(analysis_results)    
            K.clear_session()

            return jsonify({
            "status": "success",
            "predictions": inference_values
            })
        else:
            return jsonify({"status": "Request failed, upload pcap metadata for analysis."})
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    except RequestEntityTooLarge as large_request:
        return jsonify({
            'status': 'Upload File Size Exceeds %s' % app.config['MAX_CONTENT_LENGTH'],
            'message': str(large_request)
        }), 500

@app.post("/json_inference")
async def rest_prediction():
    try:
        if request.method == 'POST':
        
            data_value = await request.get_json()

            if data_value['packet_data']:

                json_data = dict(data_value)

                # JSON preprocessing for prediction
                X_input = preprocess_input(json_data=data_value['packet_data'])

                # Response conversion to JSON
                prediction = predict(processed_input=X_input)
                inference_value = json.dumps(prediction)
            else:
                return jsonify({"Error": "Packet data missing for threat assessment"})

            K.clear_session()

            return jsonify({
                "status": "success",
                "predictions": inference_value
            })
        else:
            return jsonify({"Error": "Submit POST request with packet metadata in JSON format"})
    
    except Exception as e:
         return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    
@app.post("/register")
async def probe_registration():
    try:
        data_value = await request.get_json()
        if data_value:
            probe_dict = json.loads(data_value)

            probe_json = json.dumps(probe_dict)

            print(probe_json, flush=True)

            print(probe_dict, flush=True)
               

            #db_upload = await db.upload_db_data(id=probe_id, data=probe_data)
            #print(db_upload, flush=True)
        
            #db_query_value = await db.get_db_data(match="nmp*")
            #print(db_query_value, flush=True)

        return probe_json
    except TypeError as error:
        return {'TypeError' :  str(error)}
    except Exception as e:
        return {'Exception' :  str(e)}
    except asyncio.CancelledError as can_error:
        return {'Exception' :  str(can_error)}
    
@app.post("/rmprobe")    
async def probe_removal():
    try:
        data_value = await request.get_json()
        if data_value:

            probe_to_rm = json.dumps(data_value)

            if probe_to_rm['confirm'] == 'y':
                print(probe_to_rm['id'])

        return probe_to_rm #status
    except TypeError as error:
        return {'TypeError' :  str(error)}
    except Exception as e:
        return {'Exception' :  str(e)}
    
@app.post("/netmetadata")
async def probe_webhook():
    try:
        data = await request.get_json()
        if data:
            msg = json.dumps(data)

            evt_data = json.loads(msg)

            print(evt_data)

        else:
            raise Exception('Ensure JSON message is attached to the request')
    except Exception as e:
        return {'Error' : e}
    finally:
        return {'try_catch_end' : 'Check the frontend UI'}
    
@app.post("/isup")
async def check_uptime():
    host_check = Uptime()
    try:
        data = await request.get_json()
        if data:
            msg = json.dumps(data)
            id_match="nmp*"
            toplink='probes'
            db_query_value = await db.get_db_data(top_link=toplink, match=id_match)

            host_probes = jsonify(db_query_value)

            print(host_probes)

            for prof in host_probes:

                if prof['hst_nm'] == msg['host']:
                    if msg['port']:
                        host_check.run(host=prof['ip'], port=prof['port'])

                    if msg['maxCount']:
                        host_check.run(host=prof['ip'], maxCount=prof['maxCount'])

                    if msg['port'] and msg['maxCount']:
                        host_check.run(host=prof['ip'], maxCount=prof['maxCount'], port=prof['port'])

            host_check.run(host=msg['ip'])

    except Exception as e:
        return jsonify({"Uptime Check Run Error" : e})
    
@app.get("/allprobes")
async def get_all_probes():
    try:

        id_match = "nmp*"
        db_query_value = await db.get_db_data(match=id_match)

        # Return JSON response
        return jsonify(db_query_value)

    except Exception as e:
        return jsonify({"Error": e })

    

def preprocess_input(json_data):
    # JSON -> Pandas DataFrame 
    df = pd.DataFrame([json_data])

    # Scaling features before running predictions
    features = ['avg_ipt', 'bytes_in', 'bytes_out', 'dest_ip',	'entropy', 'num_pkts_out', 'num_pkts_in', 'proto', 'src_ip', 'time_end', 'time_start', 'total_entropy', 'duration', 'src_port', 'dest_port'] 
    df_cleaned = df[features].fillna(0)  # Fill missing values

    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_cleaned)

    return X_scaled

# Function to preprocess the data for inference
def preprocess_file_for_inference(file_path):
    # Load the data
    data = pd.read_csv(file_path)

    # Drop rows with missing values in relevant columns (src_port, dest_port)
    data_cleaned = data.dropna(subset=['src_port', 'dest_port'])

    # Retain the original data for analysis after predictions
    original_data = data_cleaned.copy()

    # Drop the label column if present (in this case, for inference)
    if 'label' in data_cleaned.columns:
        data_cleaned = data_cleaned.drop(columns=['label'])

    # Scale the numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data_cleaned)

    return X_scaled, original_data

def predict(processed_input=None):
    # Model determines if packet is malicious, benign or outlier
    predictions = model.predict(processed_input)

    # Prediction -> binary conversion (benign, malicious, outlier)
    predicted_classes = np.argmax(predictions, axis=1)

    # Response conversion to JSON
    prediction = predicted_classes.tolist()
    inference_value = json.dumps(prediction)
    return inference_value

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run() -> None:
    app.run()


    