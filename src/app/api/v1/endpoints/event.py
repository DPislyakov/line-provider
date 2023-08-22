import time
from typing import List

from fastapi import APIRouter

from src.app.core.exceptions import NotFoundError, InvalidDataError
from src.app.models.tortoise.event import EventState

from src.app.selectors.event import EventSelector
from src.app.services.event import EventService
from src.app.schemas.event import (EventOutSchema, EventCreateSchema)

router = APIRouter()


@router.post('', response_model=EventOutSchema)
async def event_create(
        event_detail: EventCreateSchema
):
    """
    Создание события
    :param event_detail: Объект События
    :return: Объект События
    """
    event = await EventService().create(coefficient=event_detail.coefficient,
                                        deadline=int(time.time()) + event_detail.deadline,
                                        state=event_detail.state)
    if event is None:
        raise InvalidDataError(detail="Event data is invalided.")
    return event


@router.get('/{event_uuid}', response_model=EventOutSchema)
async def event_get(
        event_uuid: str
):
    """
    Получение конкретного события.
    :param event_uuid: Идентификатор События.
    :return: Объект События.
    """
    event = await EventSelector.get(uuid=event_uuid)

    if event is None:
        raise NotFoundError(detail=f"Not found event with uuid = {event_uuid}")
    return event


@router.get('', response_model=List[EventOutSchema])
async def events_get():
    """
    Получение списка всех событий.
    :return: Список Событий.
    """
    return await EventSelector.list_get_all()


@router.post('/{event_uuid}/change_to_win', response_model=EventOutSchema)
async def event_change_to_win(
        event_uuid: str
):
    """
    Изменение статуса События на Победу.
    :param event_uuid: Идентификатор События.
    :return: Объект События.
    """
    event = await EventSelector.get(uuid=event_uuid)

    if event is None:
        raise NotFoundError(detail=f"Not found event with uuid = {event_uuid}")

    event.state = EventState.FINISHED_WIN
    await event.save()
    return event


@router.post('/{event_uuid}/change_to_lose', response_model=EventOutSchema)
async def event_change_to_lose(
        event_uuid: str
):
    """
    Изменение статуса События на Поражение.
    :param event_uuid: Идентификатор События.
    :return: Объект События.
    """
    event = await EventSelector.get(uuid=event_uuid)

    if event is None:
        raise NotFoundError(detail=f"Not found event with uuid = {event_uuid}")

    event.state = EventState.FINISHED_LOSE
    await event.save()
    return event
