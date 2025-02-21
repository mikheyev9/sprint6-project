import time

from functional.settings import redis_settings
from redis import Redis

if __name__ == "__main__":
    redis_client = Redis(host=redis_settings.host, port=redis_settings.port)
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
