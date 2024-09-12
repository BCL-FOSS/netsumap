from quart import request
import json
from init_app import app
import websocket
from websocket import create_connection
from models.UniFiNetAPI import UniFiNetAPI
from models.util_models.PDF import PDF
from models.util_models.Utility import Utility
from models.util_models.RedisDB import RedisDB
import asyncio
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor()

@app.post("/nd_login")
async def ubnt_auth():
    try:

        loop = asyncio.new_event_loop()
        
        data_value = loop.run_until_complete(request.get_json())

        if data_value:
            print('Data coroutine complete')
            json_data = json.dumps(data_value)
            data = json.loads(json_data)
            
            print(data)        

        ubnt_profile = UniFiNetAPI(controller_ip=data['ip'], controller_port=data['port'], username=data['username'], password=data['password'])

        profile_value = await ubnt_profile.authenticate()

        db = RedisDB()    

        db_connect = await db.connect_to_db(db_host_name=app.config['REDIS_DB'])
        print(db_connect)

        #db_upload = await db.upload_nd_profile(user_id=profile_value['id'], user_data=profile_value)
        #print(db_upload)

        return profile_value

    except TypeError as error:
        return {'TypeError' :  str(error)}
    except Exception as e:
        return {'Exception' :  str(e)}

@app.get("/nd_redis")    
async def redis():
    try:
        db = RedisDB()    

        db_connect = await db.connect_to_db(db_host_name=app.config['REDIS_DB'])

        return db_connect
    except TypeError as error:
        return {'TypeError' :  str(error)}
    except Exception as e:
        return {'Exception' :  str(e)}

@app.post("/unifi_webhook")
async def webhook():
    try:
        data = await request.get_json()
        if data:
            data = json.dumps(data)
            #unifi_event = {
            #    "message": str(data)
            #}
            ws = activate_websocket()
            await ws.send(str(data))
        else:
            raise Exception('Ensure JSON message is attached to the request')
    except Exception as e:
        return {'Error' : e}
    finally:
        return {'try_catch_end' : 'Check the frontend UI'}

def activate_websocket():
    websocket.enableTrace = True
    ws=create_connection(app.config['WEBSOCKET_ADDRESS'])
    return ws

def run() -> None:
    try:

        app.run()

    except OSError as oserror:
        return{"Application Server Error": "Server is already running. Please stop and restart the service.\n" + str(oserror)}