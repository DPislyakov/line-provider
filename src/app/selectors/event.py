from src.app.selectors.utils import TortoiseSelector

from src.app.models.pydantic.event import Event_Pydantic
from src.app.models.tortoise.event import Event, EventState


class EventSelector(TortoiseSelector[Event, Event_Pydantic]):
    model = Event
    pydantic_model = Event_Pydantic
    id_field = 'uuid'

    @classmethod
    async def list_get_active(cls):
        return await cls.list_get(state=EventState.NEW)

    @classmethod
    async def list_get(cls, **kwargs):
        return await cls.list_get_as_qs(**kwargs)

    @classmethod
    def list_get_as_qs(cls, **kwargs):
        return cls.model.filter(**kwargs)
