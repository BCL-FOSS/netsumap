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

# init Redis DB connection
#db = RedisDB(hostname=app.config['REDIS_DB'], port=app.config['REDIS_DB_PORT'])  

K.clear_session() # Clears GPU resources before loading model

# Load model defined in config file
model = load_model(app.config['MODEL'])  

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
    
@app.post("/threat_analysis")
async def prediction():
    try:
        
        data_value = await request.get_json()

        if data_value['packet_data']:

            json_data = dict(data_value)

            # JSON preprocessing for prediction
            X_input = preprocess_input(json_data=data_value['packet_data'])

            # Model determines if packet is malicious, benign or outlier
            predictions = model.predict(X_input)

            # Prediction -> binary conversion (benign, malicious, outlier)
            predicted_classes = np.argmax(predictions, axis=1)

            """
                if data_value['user_id']:
                db_query_value = await db.get_profile(key=data_value['user_id'])
                ubnt_profile = UniFiNetAPI(controller_ip=db_query_value['url'], controller_port=db_query_value['port'], username=db_query_value['username'], password=data['password'])
                ubnt_profile.token = db_query_value['token']
                ubnt_profile.id = db_query_value['id']
                command = await ubnt_profile.mgr_devices()
            
            """

            # Response conversion to JSON
            prediction = predicted_classes.tolist()
            inference_value = json.dumps(prediction)
        else:
            return jsonify({"Error": "Packet data missing for threat assessment"})

        K.clear_session()

        return jsonify({
            "status": "success",
            "predictions": inference_value
        })
    
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

def run() -> None:
    app.run()


    