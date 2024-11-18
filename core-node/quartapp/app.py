from quart import request, render_template, jsonify
import json
from init_app import app
from models.util.Uptime import Uptime
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


# init Redis DB connection
db = app.config['DB_CONN']

K.clear_session() # Clears GPU resources before loading model

# Load model defined in config file

# model = load_model(app.config['MODEL'])  

@app.route('/favicon.ico')
async def favicon():
    return '', 204  # Respond with an empty response and 204 status (No Content)

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
    return await render_template("blank.html")

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
    file = (await request.files)['file']
    

    if file:
        print('CSV file attached', flush=True)
    else:
        return jsonify({"message": "No file uploaded"}), 400
        
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    (await request.files['file'].save(filename))

    #result = await file.save(file_path)

    """
        X_inference, original_data = preprocess_file_for_inference(file_path=file_path)
                    
        inference_value = predict(processed_input=X_inference)
    
    """
    return jsonify({"message": f"{filename} uploaded successfully!"})

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
        await db.ping_db()
        data_value = await request.get_json()
        if data_value:
            print(data_value, flush=True)

            # Extract specific fields from the JSON data
            probe_id = data_value["id"]
            probe_ip = data_value["ip"]
            host_name = data_value["hst_nm"]

            # Example debug output of extracted values
            print(f"Probe ID: {probe_id}", flush=True)
            print(f"Probe Data: {probe_ip}", flush=True)
            print(f"Host Name: {host_name}", flush=True)

            db_upload = await db.upload_db_data(id=probe_id, data=data_value)
            
            print(db_upload, flush=True)
        
            db_query_value = await db.get_obj_data(key=probe_id)
            print(db_query_value, flush=True)

        return jsonify({
                "id": probe_id,
                "probe_data": probe_ip,
                "host_name": host_name
            })
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
    
@app.route("/isup")
async def check_uptime():
    host_check = Uptime()
    probe_id = request.args.get('probe_id', '')

    try:
        id_match="nmp*"
        toplink='probes'
        db_query_value = await db.get_db_data(match=id_match)

        for probe in db_query_value:
            if probe == probe_id:
                host_check.check_service()


    except Exception as e:
        return jsonify({"Uptime Check Run Error" : e})
    
@app.route('/all_probes')
async def all_probes():
    await db.ping_db()
    match = "nmp*"
    db_query_value = await db.get_all_data(match=match)

    if db_query_value:
        print(json.dumps(db_query_value), flush=True)
    else:
        print('DB retrieval failed', flush=True)

    # Return JSON response
    return db_query_value

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

def test_func():
    return "from quart"

def run() -> None:
    app.run()


    