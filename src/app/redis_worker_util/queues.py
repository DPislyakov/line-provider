import random
import time

from src.app.models.tortoise.event import Event, EventState
from src.app.selectors.event import EventSelector
from app.config import common_config


async def change_event_status(event: Event, redis) -> None:
    if time.time() > event.deadline:
        event.state = random.choice([EventState.FINISHED_WIN, EventState.FINISHED_LOSE])
        await event.save()
        item = await redis.hget(common_config.EVENT_ACTIVE_HM,
                                str(event.uuid))
        if item:
            await redis.hset(common_config.EVENT_FINISHED_HM,
                             str(event.uuid),
                             int(event.state))
            await redis.hdel(common_config.EVENT_ACTIVE_HM,
                             str(event.uuid))
    else:
        item = await redis.hget(common_config.EVENT_ACTIVE_HM,
                                str(event.uuid))
        if not item:
            await redis.hset(common_config.EVENT_ACTIVE_HM,
                             str(event.uuid),
                             f"{event.coefficient}-{event.deadline}")
    return None


async def update_queues(redis) -> None:
    active_event = await EventSelector.list_get_active()
    print([event.uuid for event in active_event])
    for event in active_event:
        await change_event_status(event, redis)
    return None
