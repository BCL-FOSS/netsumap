
    


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
    
