import json
import websockets

from flask import Response, render_template, request, Flask

import config
from init_app import app

async def send_message(message):
    async with websockets.connect(config.WEBSOCKET_URL) as websocket:
        await websocket.send(message)

@app.route('/site_dpi_listener', methods=['POST'])
def unifi_webhook():
    if request.method == "POST":
        data = request.get_json()
        if data:
            msg = json.dumps(data)
            unifi_event = {
                "uid":"",
                "type": "",
                "message": msg,
            }
            send_message(unifi_event)
        else:
            return 'failed'

@app.route('/sta_dpi_listener', methods=['POST'])
def unifi_webhook():
    if request.method == "POST":
        data = request.get_json()
        if data:
            msg = json.dumps(data)
            unifi_event = {
                "uid":"",
                "type": "",
                "message": msg,
            }
            send_message(unifi_event)

        else:
            return 'failed'
        
@app.route('/event_listener', methods=['POST'])
def unifi_webhook():
    if request.method == "POST":
        data = request.get_json()
        if data:
            msg = json.dumps(data)
            unifi_event = {
                "uid":"",
                "type": "",
                "message": msg,
            }
            send_message(unifi_event)

        else:
            return 'failed'
        
@app.route('/alarm_listener', methods=['POST'])
def unifi_webhook():
    if request.method == "POST":
        data = request.get_json()
        if data:
            msg = json.dumps(data)
            unifi_event = {
                "uid":"",
                "type": "",
                "message": msg,
            }
            send_message(unifi_event)

        else:
            return 'failed'


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)
