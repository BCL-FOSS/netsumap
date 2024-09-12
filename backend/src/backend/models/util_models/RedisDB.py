import redis
import asyncio
import asyncio_redis

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

            return {"DB Upload Status" : "Profile %s Upload Complete" % user_id}
        except Exception as e:
            return {"DB Upload Error":str(e)}
        
    async def retrieve_profile(self, id=''):
        try: 
            # Connect to the locally installed Redis database
            connection = await asyncio_redis.Connection.create(host=self.host_name, port=self.port)


            # Use HMSET to upload a hashset representing the user's profile

            await connection.hmget(id)
    
            # Close the connection
            connection.close()

            return {"DB Upload Status" : ""}
        except Exception as e:
            return {"DB Upload Error":str(e)}
        
    async def get_profile(self, key: str):
        """
    Retrieve a hashmap from Redis by its key.

    :param key: The key under which the hashmap is stored.
    :return: The hashmap as a dictionary, or an error message if not found.
    """
        try:
            # Connect to the locally installed Redis database
            connection = await asyncio_redis.Connection.create(host=self.host_name, port=self.port)
    
            # Check if the key exists and is a hash
            key_type = await connection.type(key)
    
            if key_type != 'hash':
            # If the key doesn't exist or is not a hash
                connection.close()
                return {"Search Query Error": f'Key "{key}" does not exist or is not a hashmap.'}
    
            # Retrieve all fields and values of the hashmap
            hashmap = await connection.hgetall_asdict(key)
    
            # Close the Redis connection
            connection.close()
    
            # Convert the hashmap values from bytes to strings
            decoded_hashmap = {k: v.decode('utf-8') for k, v in hashmap.items()}
            
            return decoded_hashmap
        except Exception as e:
            return {"Search Process Error": e}
    
        

