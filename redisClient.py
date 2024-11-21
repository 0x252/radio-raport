import redis, os
class RedisSingleton:
    _i = None
    def __new__(c):
        if c._i is None:
            c._i = super(RedisSingleton, c).__new__(c) 
            c._i.client_ = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=os.getenv("REDIS_PORT"),
                password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True
                )
            return c._i
        return c._i
        
    def get_client(s):
        return s._i.client
    @property
    def client(s):
        return s._i.client_
    