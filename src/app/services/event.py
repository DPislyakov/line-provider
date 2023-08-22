import tortoise.exceptions

from src.app.services.utils import TortoiseService
from src.app.models.pydantic.event import Event_Pydantic
from src.app.models.tortoise.event import Event


class EventService(TortoiseService[Event, Event_Pydantic]):
    model = Event
    pydantic_model = Event_Pydantic

    async def create(self, **kwargs) -> Event:
        try:
            return await super(EventService, self).create(**kwargs)
        except tortoise.exceptions.IntegrityError as e:
            print(e)

    async def update(self, **kwargs) -> Event:
        return await super(EventService, self).update(**kwargs)
