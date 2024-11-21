import redis, os
class RedisSingleton:
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls) 
            cls._instance._client = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"), 
                port=int(os.getenv("REDIS_PORT", 6379)),
                password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True
            )
        return cls._instance

    @property
    def client(self):
        return self._client
