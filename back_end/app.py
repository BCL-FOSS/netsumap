#app_producer.py
import json
import websockets
from quart import Quart

from flask import Response, render_template, request, Flask
from ubiquipy import UniFiAPI

import config
from init_app import app


async def send_message(message):
    async with websockets.connect(config.WEBSOCKET_URL) as websocket:
        await websocket.send(message)

@app.route("/login", methods=['POST'])
def login():
    if request.method == "POST":
        data = request.get_json()
        if data:
            unifi_connect = 
            
@app.route("/site_dpi", methods=['POST'])
def unifi_site_dpi():
    if request.method == "POST":
        data = request.get_json()
        if data:
            print("received data =", data)
            unifi_connect = 
            ubnt_data = unifi_connect.get_sitedpi_data()
            unifi_event = {
                "uid":"",
                "type": "",
                "message": ubnt_data,
            }
            send_message(unifi_event)
        else:
            return 'failed'    



        
@app.route("/sta_dpi", methods=['POST'])
def unifi_sta_dpi():
    if request.method == "POST":
        data = request.get_json()
        if data:
            print("received data =", data)
            unifi_connect = 
            ubnt_data = unifi_connect.get_stadpi_data()
            unifi_event = {
                "uid":"",
                "type": "",
                "message": ubnt_data,
            }
            send_message(unifi_event)
        else:
            return 'failed'
          
        

        
@app.route("/events", methods=['POST'])
def unifi_sta_dpi():
    if request.method == "POST":
        data = request.get_json()
        if data:
            print("received data =", data)
            unifi_connect = 
            ubnt_data = unifi_connect.get_event_data()
            return ubnt_data
        

        
@app.route("/alarms", methods=['POST'])
def unifi_sta_dpi():
    if request.method == "POST":
        data = request.get_json()
        if data:
            print("received data =", data)
            unifi_connect = 
            ubnt_data = unifi_connect.get_alarm_data()
            return ubnt_data
        



if __name__ == "__main__":
   app.run(host="0.0.0.0",port=5000, debug=True)
