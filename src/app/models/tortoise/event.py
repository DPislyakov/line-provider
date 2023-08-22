from tortoise import fields
from tortoise.models import Model
from enum import IntEnum


class EventState(IntEnum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class Event(Model):
    uuid = fields.UUIDField(pk=True)
    coefficient = fields.DecimalField(max_digits=22, decimal_places=11, null=True)
    deadline = fields.IntField(null=True)
    state = fields.IntEnumField(EventState)

    def __str__(self):
        return f'{self.uuid} ({self.state})'

    class Meta:
        ordering = ['deadline']
