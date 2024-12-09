import redis
import json

class RedisDB:
   
    def __init__(self, hostname='', port='', username='', password=''):
        self.host_name=hostname
        self.port=port
        self.user_name=username
        self.pass_word=password
        # setup async connection to Redis container
        self.redis_conn = redis.Redis.from_url(
            f"redis://{self.host_name}:{self.port}", encoding="utf-8", decode_responses=True
        )
        if isinstance(self.redis_conn, redis.Redis) is False:
            return print('Initial Redis connection failed.', flush=True)
        else:
            print(self.redis_conn, flush=True)

    def ping_db(self):
        try:
            # Create Redis connection
            pong = self.redis_conn.ping()
            
            print(pong, flush=True)
            
        except Exception as e:
            return {"DB Connection Error":str(e)}
        finally:
            self.redis_conn.close()
    

    def upload_db_data(self, id = '', data = {}):
        try: 
            
            str_hashmap = {str(k): str(v) for k, v in data.items()}

            # HSET probe data
            result = self.redis_conn.hset(id, mapping=str_hashmap)
    
            return result #{"DB Upload Status" : "Profile ID %s upload successful" % id}
        except Exception as e:
            return {"DB Upload Error":str(e)}
        finally:
            self.redis_conn.close()

    def get_all_data(self, match='*'):
        try:
            all_data = {}
            cursor = b'0'  # Start the SCAN with cursor 0

            # Use SCAN to fetch keys in batches
            cursor, keys = self.redis_conn.scan(cursor=cursor, match=match)
            for key in keys:
                print(key, flush=True)
                # Retrieve the hash data for each key
                hash_data = self.redis_conn.hgetall(key)
                all_data[key] = {k: v for k, v in hash_data.items()}

            # Print or process all retrieved data
            print(all_data, flush=True)
            return all_data

        except Exception as e:
            print(f"Error retrieving data: {e}", flush=True)
            return None

        finally:
            self.redis_conn.close()

    def get_obj_data(self, key=''):
        try:

            probe = self.redis_conn.hgetall(key)

            if probe:
                return probe
            else:
                return {"error":"search failed"}
                
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.redis_conn.close()
        

