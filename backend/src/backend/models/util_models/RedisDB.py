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

    async def connect_to_db(self):
        try:
            
            # Create Redis connection
            connection = await asyncio_redis.Connection.create(host=self.host_name, port=self.port)

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
            connection = await asyncio_redis.Connection.create(host=self.host_name, port=self.port)

            str_hashmap = {str(k): str(v) for k, v in user_data.items()}

            # Use HMSET to upload a hashset representing the user's profile

            await connection.hmset(user_id, str_hashmap)
    
            # Close the connection
            connection.close()

            return {"DB Upload Status" : "Profile ID %s upload successful" % user_id}
        except Exception as e:
            return {"DB Upload Error":str(e)}
    
    async def get_profile(self, key=None):
        try:
            """
                Retrieve an entire hashmap from Redis using the HGETALL command.

                :param key: The key of the hashmap.
                :return: A dictionary of field-value pairs or an error message if the key does not exist.
            """
            # Connect to the locally installed Redis database
            connection = await asyncio_redis.Connection.create(host=self.host_name, port=self.port)
    
            # Check if the key exists and is a hash
            key_type = await connection.type(key)
    
            if key_type != 'hash':
                # If the key doesn't exist or is not a hashmap
                connection.close()
                return f'Key "{key}" does not exist or is not a hashmap.'
    
            # Retrieve all fields and values from the hashmap using HGETALL
            hashmap = await connection.hgetall_asdict(key)
    
            # Close the Redis connection
            connection.close()
    
            # Convert the byte values to strings (since Redis returns values as bytes)
            decoded_hashmap = {field: value for field, value in hashmap.items()}
    
            return decoded_hashmap
        except Exception as e:
            return {"DB Query Error" : str(e)}
        

