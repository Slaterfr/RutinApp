import time
import json

from ..logging.loggerservice import logger
from .redisconfig import redis_client


class RedisService:
    async def caching_aside(self,key, fetch_funct, ttl : int = 500):
        start = time.perf_counter()

        logger.info(f"SEARCHING CACHE FOR: {key}")

        data = redis_client.get(key)
        
        if data:
            logger.info(f"CACHE HIT ON KEY: {key}")
            elapsed = (
                time.perf_counter() - start
            ) * 1000

            logger.info(
                f"Cache request completed in "
                f"{elapsed:.2f}ms"
            )

            return json.loads(data)
        
        logger.warning(f"CACHE MISS ON KEY: {key}")

        fetch_data = await fetch_funct()

        redis_client.set(key, json.dumps(fetch_data), ex=ttl)

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        logger.info(
            f"DB request completed in "
            f"{elapsed:.2f}ms"
        )

        return fetch_data

    async def caching(self, key, fecth_funct, ttl : int = 300):
        data = redis_client.get(key)
        if data:
            logger.info(f"CACHE HIT FOR KEY {key}")
            return json.loads(data)
        
        logger.info(f"CACHE MISS FOR KEY {key}")
        fetched = await fecth_funct()
        redis_client.set(key, json.dumps(fetched), ex=ttl)

        return fetched
        
