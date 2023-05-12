from redis import Redis

from tests.functional.utils.settings_wait_for import RedisSettings
from tests.functional.utils.backoff import check_connection

if __name__ == '__main__':
    config = RedisSettings()  # type: ignore
    red_client = Redis(
        host=config.redis_host, port=config.redis_port
    )
    check_connection(red_client)
