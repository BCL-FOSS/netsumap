import redis
import config

class RedisAPI:

    db_connection = redis.Redis(host='localhost', port=6380, username= config.REDIS_USER, password=config.REDIS_PASSWORD, decode_responses=True)
    db_connection.ping()

    def store():
        

