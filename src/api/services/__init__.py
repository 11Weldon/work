import os
import redis.asyncio as aioredis
from zappware.operator_facade import OperatorFacade

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', '6380')

redis_client = aioredis.from_url(f"redis://{redis_host}:{redis_port}")
#убрать пототм
FACADES = {
    "lab": {
        "TotalVideo": {
            "name": "lab.TotalVideo",
            "base_url": "http://10.251.0.10:8889/op_facade",
            "username": "admin",
            "password": "a12017",
        }
    }
}
#
ofparams = FACADES["lab"]["TotalVideo"]
of = OperatorFacade.from_endpoint(**ofparams)
