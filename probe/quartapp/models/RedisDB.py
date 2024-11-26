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

    async def get_all_data(self, match='*'):
        try:
            all_data = {}
            cursor = b'0'  # Start the SCAN with cursor 0

            # Use SCAN to fetch keys in batches
            cursor, keys = await self.redis_conn.scan(cursor=cursor, match=match)
            for key in keys:
                print(key, flush=True)
                # Retrieve the hash data for each key
                hash_data = await self.redis_conn.hgetall(key)
                all_data[key] = {k: v for k, v in hash_data.items()}

            # Print or process all retrieved data
            print(all_data, flush=True)
            return all_data

        except Exception as e:
            print(f"Error retrieving data: {e}", flush=True)
            return None

        finally:
            await self.redis_conn.close()


    """
        async def get_all_data(self, match=''):
        try:
            probes=[]
            nmp_hashes = {}
            retrieved_probes = await self.redis_conn.scan(match=match)

            if retrieved_probes:
                print(retrieved_probes, flush=True)

            for value in retrieved_probes:
                counter, key_list = value
                for key in key_list:
                    hash_data = await self.redis_conn.hgetall(key)
                    print(hash_data, flush=True)
                #nmp_hashes[probe] = hash_data
                    

            #return nmp_hashes
    

            

        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            await self.redis_conn.close()
    """
        
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
        

