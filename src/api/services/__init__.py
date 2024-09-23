import os
import redis.asyncio as aioredis

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', '6381')

redis_client = aioredis.from_url(f"redis://{redis_host}:{redis_port}")