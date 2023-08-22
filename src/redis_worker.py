import asyncio
import aioredis
from tortoise import Tortoise

from app.config import common_config
from app.redis_worker_util.queues import update_queues
from db import tortoise_config


async def redis_work():

    await Tortoise.init(
        db_url=tortoise_config.db_url,
        modules={"models": ["aerich.models",
                            "app.models.tortoise.event"]}
    )

    redis = await aioredis.create_redis_pool(f'redis://{common_config.REDIS_HOST}'
                                             f':{common_config.REDIS_PORT}')
    while True:
        await update_queues(redis)
        await asyncio.sleep(common_config.EVENT_UPDATE_TIMEOUT)
    redis.close()
    await redis.wait_closed()


if __name__ == '__main__':
    asyncio.run(redis_work())
