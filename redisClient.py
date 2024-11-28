import redis, os
from urllib.parse import urlparse

class RedisSingleton:
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            redis_url = os.getenv("REDIS_URL")
            parsed_url = urlparse(redis_url)
            cls._instance = super().__new__(cls) 
            print(f'connect to {parsed_url.hostname}:{parsed_url.port}')
            cls._instance._client = redis.Redis(
                host=parsed_url.hostname or "localhost",
                port=parsed_url.port or 6379,
                password=parsed_url.password,
                decode_responses=True
            )

        return cls._instance

    @property
    def client(self):
        return self._client
