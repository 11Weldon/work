import os
import redis.asyncio as aioredis
from operatorfacade.src.zappware.operator_facade import OperatorFacade
import yaml

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', '6379')

redis_client = aioredis.from_url(f"redis://{redis_host}:{redis_port}")

config_path = os.path.join(os.path.dirname(__file__), '../../..', 'config.yml')
with open(config_path, 'r') as f:
    FACADES = yaml.safe_load(f)

ofparams = FACADES["lab"]["TotalVideo"]
of = OperatorFacade.from_endpoint(**ofparams)
