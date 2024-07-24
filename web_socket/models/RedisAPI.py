import redis

class RedisAPI:

    db_connection = redis.Redis(host='localhost', port=6380, username='dvora', password='redis', decode_responses=True)
    db_connection.ping()

    def store():
        

