from quart import request, render_template, jsonify
import json
from init_app import app
from models.UniFiNetAPI import UniFiNetAPI
#from models.util_models.RedisDB import RedisDB
import numpy as np
import asyncio
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from sklearn.preprocessing import StandardScaler
import gc

#db = RedisDB(hostname=app.config['REDIS_DB'], port=app.config['REDIS_DB_PORT'])  
K.clear_session()
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

        if data_value:
            print('Data coroutine complete')

            json_data = list(data_value)

            print(str(json_data))

            X_input = await preprocess_input(json_data=data_value)#preprocess_loop.run_until_complete(preprocess_input(data))

            predictions = model.predict(X_input)

            # Convert predictions to binary classes (benign, malicious, outlier)
            predicted_classes = np.argmax(predictions, axis=1)

            response_data = []
            for i, row in enumerate(data_value):
                response_data.append({
                    **row,
                    'predicted_class': int(predicted_classes[i])  # Convert class label to integer for JSON response
                })

        K.clear_session()

        # Return predictions as JSON response
        return jsonify({
            "status": "success",
            "predictions": response_data
        })
    except Exception as e:
         return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def preprocess_input(json_data):
    # Convert JSON data into a DataFrame
    df = pd.DataFrame.from_dict(json_data)

    # Scale the relevant features before running predictions
    features = ['avg_ipt', 'bytes_in', 'bytes_out', 'dest_ip',	'entropy', 'num_pkts_out', 'num_pkts_in', 'proto', 'src_ip', 'time_end', 'time_start', 'total_entropy', 'duration'] 
    df_cleaned = df[features].fillna(0)  # Fill missing values

    # Scale the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_cleaned)

    return X_scaled

def run() -> None:
    app.run()


    