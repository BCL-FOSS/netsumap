import redis
import asyncio
import asyncio_redis
import json

class RedisDB:
   
    def __init__(self, hostname='', port='', username='', password=''):
        self.host_name=hostname
        self.port=port
        self.user_name=username
        self.pass_word=password

    async def get_redis_connection(self):
        
        return await asyncio_redis.Connection.create(host=self.host_name, port=self.port)

    async def connect_to_db(self):
        try:
            # Create Redis connection
            connection = await self.get_redis_connection()

            pong = await connection.ping()
            print(pong, flush=True)
            
        except Exception as e:
            return {"DB Connection Error":str(e)}
        finally:
            # When finished, close the connection.
            connection.close()

    async def upload_db_data(self, id = '', data = {}):
        try: 
            # Connect to the locally installed Redis database
            connection = await self.get_redis_connection()

            str_hashmap = {str(k): str(v) for k, v in data.items()}

            # Use HMSET to upload a probe data

            result = await connection.hmset(id, str_hashmap)
    
            return result #{"DB Upload Status" : "Profile ID %s upload successful" % id}
        except Exception as e:
            return {"DB Upload Error":str(e)}
        finally:
            connection.close()

        
    async def get_all_data(self, match=''):
        try:
            connection = await self.get_redis_connection()

            probe_keys = await connection.scan_iter(match)
            
            nmp_hashes = {}

            # Loop through each key and get hash data
            for key in probe_keys:
                print(key, flush=True)
                hash_data = await connection.hgetall(key)
                nmp_hashes[key] = hash_data

            return nmp_hashes

        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            connection.close()

    async def get_obj_data(self, key=''):
        try:
            connection = await self.get_redis_connection()

            probe = await connection.hgetall(key)

            return probe
                
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            connection.close()
        

