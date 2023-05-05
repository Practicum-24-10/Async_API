import time

from redis import Redis

from tests.functional.utils.settings_wait_for import RedisSettings

if __name__ == '__main__':
    config = RedisSettings()  # type: ignore
    red_client = Redis(
        host=config.redis_host, port=config.redis_port
    )
    while True:
        if red_client.ping():
            break
        time.sleep(1)
