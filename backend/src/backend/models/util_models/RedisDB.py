import redis
import asyncio
import asyncio_redis

class RedisDB:
   
    def __init__(self) -> None:
        self.r = None
        pass

    async def connect_to_db(self, db_host_name='', db_port=6379):
        try:
            
            # Create Redis connection
            connection = await asyncio_redis.Connection.create(host=db_host_name, port=db_port)

            pong = await connection.ping()
            print(pong)

            # When finished, close the connection.
            connection.close()
            
            return {"DB Connection Status": "Success"}
            
        except Exception as e:
            return {"DB Connection Error":str(e)}
        
    
    async def upload_nd_profile(self, user_id = '', user_data = {}, db_host_name='', db_port=6379):
        try: 
            # Connect to the locally installed Redis database
            connection = await asyncio_redis.Connection.create(host=db_host_name, port=db_port)

            str_hashmap = {str(k): str(v) for k, v in user_data.items()}

            # Use HMSET to upload a hashset representing the employee data

            await connection.hmset(user_id, str_hashmap)
    
            # Close the connection
            connection.close()

            return {"DB Upload Status" : "Profile %s Upload Complete" % user_id, "Upload Complete": upload}
        except Exception as e:
            return {"DB Upload Error":str(e)}

    def set_profile(self):
        try:
            self.r.hset('user-session:123', mapping={
                'name': 'John',
                "surname": 'Smith',
                "company": 'Redis',
                "age": 29
            })
        except Exception as e:
            return {"Profile -> DB Upload Error":str(e)}
