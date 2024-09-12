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
            connection = await asyncio_redis.Connection.create(host='localhost', port=6379)

            # Set a key
            ping_result = await connection.ping()

            if ping_result == True:
                return {"DB Connection Success":"Connected to Redis DB successfully"}
            elif ping_result == False:
                return {"DB Connection Failed":"Could not connect to Redis DB"}

            # When finished, close the connection.
            connection.close()
            
        except Exception as e:
            return {"DB Connection Error":str(e)}

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
