import redis
import asyncio
import asyncio_redis
import json

class RedisDB:
   
    def __init__(self, hostname='', port='', username='', password=''):
        self.host_name = hostname
        self.port = port
        self.user_name = username
        self.pass_word = password

    async def get_redis_connection(self):
        return await asyncio_redis.Connection.create(host=self.host_name, port=self.port)

    async def connect_to_db(self):
        try:
            
            # Create Redis connection
            connection = await self.get_redis_connection()

            pong = await connection.ping()
            print(pong)

            # When finished, close the connection.
            connection.close()
            
            return {"DB Connection Status": "Success"}
            
        except Exception as e:
            return {"DB Connection Error":str(e)}
        
    
    async def upload_profile(self, user_id = '', user_data = {}):
        try: 
            # Connect to the locally installed Redis database
            connection = await self.get_redis_connection()

            str_hashmap = {str(k): str(v) for k, v in user_data.items()}

            # Use HMSET to upload a hashset representing the user's profile

            await connection.hmset(user_id, str_hashmap)
    
            # Close the connection
            connection.close()

            return {"DB Upload Status" : "Profile ID %s upload successful" % user_id}
        except Exception as e:
            return {"DB Upload Error":str(e)}
        
    # Function to retrieve a hash by key
    async def get_profile(self, key: str):
        try:
            connection = await self.get_redis_connection()
            # Get all the fields and values for the given hash key
            result = await connection.hgetall_asdict(key)
            connection.close()
            return result
        except Exception as e:
            return {"error": str(e)}
        

