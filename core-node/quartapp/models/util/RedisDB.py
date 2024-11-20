import redis
import asyncio
import aioredis

import json

class RedisDB:
   
    def __init__(self, hostname='', port='', username='', password=''):
        self.host_name=hostname
        self.port=port
        self.user_name=username
        self.pass_word=password
        # setup async connection to Redis container
        self.redis_conn = aioredis.from_url(
            f"redis://{self.host_name}:{self.port}", encoding="utf-8", decode_responses=True
        )
        if self.redis_conn is None:
            return print('Initial Redis connection failed.', flush=True)
        else:
            print(self.redis_conn, flush=True)

    async def ping_db(self):
        try:
            # Create Redis connection
            pong = await self.redis_conn.ping()
            
            print(pong, flush=True)
            
        except Exception as e:
            return {"DB Connection Error":str(e)}
        finally:
            await self.redis_conn.close()
    

    async def upload_db_data(self, id = '', data = {}):
        try: 
            
            str_hashmap = {str(k): str(v) for k, v in data.items()}

            # HSET probe data
            result = await self.redis_conn.hset(id, mapping=str_hashmap)
    
            return result #{"DB Upload Status" : "Profile ID %s upload successful" % id}
        except Exception as e:
            return {"DB Upload Error":str(e)}
        finally:
            await self.redis_conn.close()
        
    async def get_all_data(self, match=''):
        try:
            probes=[]
            nmp_hashes = {}
            retrieved_probes = await self.redis_conn.scan(match=match)
            for probe in retrieved_probes:
                print(probe, flush=True)
                probes.append(probe)
                hash_data = await self.redis_conn.hgetall(probe)
                nmp_hashes[probe] = hash_data

            return nmp_hashes

        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            await self.redis_conn.close()

    async def get_obj_data(self, key=''):
        try:

            probe = await self.redis_conn.hgetall(key)

            if probe:
                return probe
            else:
                return {"error":"search failed"}
                
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            await self.redis_conn.close()
        

