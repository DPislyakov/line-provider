from typing import Optional
from pydantic import BaseModel
import decimal

from src.app.models.pydantic.event import Event_Pydantic
from src.app.models.tortoise.event import EventState


class EventCreateSchema(BaseModel):
    coefficient: Optional[decimal.Decimal]
    deadline: Optional[int]
    state: Optional[EventState] = EventState.NEW


class EventOutSchema(Event_Pydantic):
    pass

