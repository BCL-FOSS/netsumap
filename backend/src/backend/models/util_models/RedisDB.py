import redis

class RedisDB:
   
    def __init__(self) -> None:
        self.r = None
        pass

    def connect_to_db(self, db_host_name='', db_port=6379):
        try:
            self.r = redis.Redis(host=db_host_name, port=db_port, decode_responses=True)
            ping_result = self.r.ping()
            if ping_result == True:
                return {"DB Connection Success":"Connected to Redis DB successfully"}
            elif ping_result == False:
                return {"DB Connection Failed":"Could not connect to Redis DB"}
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
