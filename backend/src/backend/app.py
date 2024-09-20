from quart import request, render_template, jsonify
import json
from init_app import app
import websocket
from websocket import create_connection
from models.UniFiNetAPI import UniFiNetAPI
from models.util_models.RedisDB import RedisDB
import asyncio

db = RedisDB(hostname=app.config['REDIS_DB'], port=app.config['REDIS_DB_PORT'])  

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

@app.post("/login")
async def authentication():
    try:
        loop = asyncio.new_event_loop()
        
        data_value = loop.run_until_complete(request.get_json())

        if data_value:
            print('Data coroutine complete')
            json_data = json.dumps(data_value)
            data = json.loads(json_data)
            
            #print(data)    

        loop.close()        
            
        ubnt_profile = UniFiNetAPI(controller_ip=data['ip'], controller_port=data['port'], username=data['username'], password=data['password'])

        profile_value = await ubnt_profile.authenticate()

        db_upload = await db.upload_profile(user_id=profile_value['id'], user_data=profile_value)
        print(db_upload)
    
        db_query_value = await db.get_profile(key=profile_value['id'])
        #print(db_query_value)

        return db_query_value
                #{"Auth_Status" : "Success",
                #"Profile_Data" : db_query_value}
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
        
        db_query_value = await db.get_profile(key=data['id'])

        ubnt_profile = UniFiNetAPI(controller_ip=db_query_value['url'], controller_port=db_query_value['port'], username=db_query_value['username'], password=data['password'])
        ubnt_profile.token = db_query_value['token']
        ubnt_profile.id = db_query_value['id']
        status = await ubnt_profile.sign_out()

        return status
    except TypeError as error:
        return {'TypeError' :  str(error)}
    except Exception as e:
        return {'Exception' :  str(e)}
    finally:
        await ubnt_profile.ubiquipy_client_session.close()
    

@app.post("/ubnt_stats")
async def get_health_data():
    try:
        loop = asyncio.new_event_loop()
        
        data_value = loop.run_until_complete(request.get_json())

        if data_value:
            print('Data coroutine complete')
            json_data = json.dumps(data_value)
            data = json.loads(json_data)
            
            print(data)    

        loop.close()   
        
        db_query_value = await db.get_profile(key=data['id'])

        ubnt_profile = UniFiNetAPI(controller_ip=db_query_value['url'], controller_port=db_query_value['port'], username=db_query_value['username'], password=data['password'])
        ubnt_profile.token = db_query_value['token']
        ubnt_profile.id = db_query_value['id']
        health_data = await ubnt_profile.controller_health_data()

        return health_data['data']
    except TypeError as error:
        return {'TypeError' :  str(error)}
    except Exception as e:
        return {'Exception' :  str(e)}
    
@app.post("/ubnt_info")
async def get_sysinfo():
    try:
        loop = asyncio.new_event_loop()
        
        data_value = loop.run_until_complete(request.get_json())

        if data_value:
            print('Data coroutine complete')
            json_data = json.dumps(data_value)
            data = json.loads(json_data)
            
            print(data)    

        loop.close()   
        
        db_query_value = await db.get_profile(key=data['id'])

        ubnt_profile = UniFiNetAPI(controller_ip=db_query_value['url'], controller_port=db_query_value['port'], username=db_query_value['username'], password=data['password'])
        ubnt_profile.token = db_query_value['token']
        ubnt_profile.id = db_query_value['id']
        sys_info = await ubnt_profile.get_sysinfo()

        return sys_info
    except TypeError as error:
        return {'TypeError' :  str(error)}
    except Exception as e:
        return {'Exception' :  str(e)}
    
@app.post("/ubnt_webhook")
async def webhook():
    try:
        data = await request.get_json()
        if data:
            data = json.dumps(data)
            #unifi_event = {
            #    "message": str(data)
            #}
            ws = activate_websocket_connection()
            await ws.send(str(data))
        else:
            raise Exception('Ensure JSON message is attached to the request')
    except Exception as e:
        return {'Error' : e}
    finally:
        return {'try_catch_end' : 'Check the frontend UI'}

def activate_websocket_connection():
    try:
        websocket.enableTrace = True
        ws=create_connection(app.config['WEBSOCKET_ADDRESS'])
        return ws
    except Exception as e:
        return {"Websocket Connection Error" : "Please verify the websocket server is online and accessible",
                "Error Message" : str(e)}

def run() -> None:
    app.run()


    