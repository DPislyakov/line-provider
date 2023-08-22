from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.models.tortoise.event import Event


Tortoise.init_models(["src.app.models.tortoise.event"],
                     "models")

Event_Pydantic = pydantic_model_creator(
    Event,
    name="Event"
)
