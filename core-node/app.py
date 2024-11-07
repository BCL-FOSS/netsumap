from quart import request, render_template, jsonify
import json
from init_app import app
from models.UniFiNetAPI import UniFiNetAPI
from models.util_models.RedisDB import RedisDB
import numpy as np
import asyncio
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from sklearn.preprocessing import StandardScaler
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask_cors import CORS
import os

# websocket.enableTrace = True
# ws=create_connection(app.config['WEBSOCKET_ADDRESS'])

# init Redis DB connection
#db = RedisDB(hostname=app.config['REDIS_DB'], port=app.config['REDIS_DB_PORT'])  

K.clear_session() # Clears GPU resources before loading model

# Allowed files extensions for /file_analysis 
ALLOWED_EXTENSIONS = set(['csv'])

# Load model defined in config file

#model = load_model(app.config['MODEL'])  

@app.get("/")
async def index():
    return await render_template("index.html")

@app.get("/app")
async def app_main():
    return await render_template("web_app.html")

@app.errorhandler(404)
async def page_not_found():
    return await render_template("404.html")

@app.errorhandler(500)
async def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

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

                    """
                        if data_value['user_id']:
                        db_query_value = await db.get_profile(key=data_value['user_id'])
                        ubnt_profile = UniFiNetAPI(controller_ip=db_query_value['url'], controller_port=db_query_value['port'], username=db_query_value['username'], password=data['password'])
                        ubnt_profile.token = db_query_value['token']
                        ubnt_profile.id = db_query_value['id']
                        command = await ubnt_profile.mgr_devices()
            
                    """
                    
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
async def prediction():
    try:
        if request.method == 'POST':
        
            data_value = await request.get_json()

            if data_value['packet_data']:

                json_data = dict(data_value)

                # JSON preprocessing for prediction
                X_input = preprocess_input(json_data=data_value['packet_data'])

                """
                if data_value['user_id']:
                db_query_value = await db.get_profile(key=data_value['user_id'])
                ubnt_profile = UniFiNetAPI(controller_ip=db_query_value['url'], controller_port=db_query_value['port'], username=db_query_value['username'], password=data['password'])
                ubnt_profile.token = db_query_value['token']
                ubnt_profile.id = db_query_value['id']
                command = await ubnt_profile.mgr_devices()
            
                """

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
    
@app.post("/login")
async def authentication():
    try:
        loop = asyncio.new_event_loop()
        
        data_value = loop.run_until_complete(request.get_json())

        if data_value:
            print('Data coroutine complete')
            json_data = json.dumps(data_value)
            data = json.loads(json_data)     

        loop.close() 
            
        ubnt_profile = UniFiNetAPI(controller_ip=data['ip'], controller_port=data['port'], username=data['username'], password=data['password'])

        profile_value = await ubnt_profile.authenticate()

        #db_upload = await db.upload_profile(user_id=profile_value['id'], user_data=profile_value)
        #print(db_upload)
    
        #db_query_value = await db.get_profile(key=profile_value['id'])
        #print(db_query_value)

        return jsonify({"Auth_Status" : "Success",
                "Profile_Data" : profile_value})
    except TypeError as error:
        return {'TypeError' :  str(error)}
    except Exception as e:
        return {'Exception' :  str(e)}
    except asyncio.CancelledError as can_error:
        return {'Exception' :  str(can_error)}
    
@app.post("/logout")    
async def signout():
    try:
        loop = asyncio.new_event_loop()
        
        data_value = loop.run_until_complete(request.get_json())

        if data_value:
            print('Data coroutine complete')
            json_data = json.dumps(data_value)
            data = json.loads(json_data)  
            #print(data)    

        loop.close()   
        
        #db_query_value = await db.get_profile(key=data['id'])

        #ubnt_profile = UniFiNetAPI(controller_ip=db_query_value['url'], controller_port=db_query_value['port'], username=db_query_value['username'], password=data['password'])
        #ubnt_profile.token = db_query_value['token']
        #ubnt_profile.id = db_query_value['id']
        #status = await ubnt_profile.sign_out()

        return data_value #status
    except TypeError as error:
        return {'TypeError' :  str(error)}
    except Exception as e:
        return {'Exception' :  str(e)}
    
@app.post("/netmetadata")
async def webhook():
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


    