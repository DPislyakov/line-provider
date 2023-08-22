import pytest
from httpx import AsyncClient

from src.main import app
from src.app.models.tortoise.event import EventState
from .init_tortoise import async_init_db


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_simple_workflow(anyio_backend):

    await async_init_db()
    test_event = {
        "coefficient": 12.22,
        "deadline": 1000,
        "state": 1
    }

    async with AsyncClient(app=app, base_url='http://localhost') as ac:
        create_response = await ac.post('/v1/app/event', json=test_event)

    assert create_response.status_code == 200
    event_uuid = create_response.json()['uuid']

    async with AsyncClient(app=app, base_url='http://localhost') as ac:
        response = await ac.get(f'/v1/app/event/{event_uuid}')

    assert response.status_code == 200
    assert float(response.json()['coefficient']) == test_event['coefficient']
    assert response.json()['state'] == EventState.NEW

    async with AsyncClient(app=app, base_url='http://localhost') as ac:
        response = await ac.post(f'/v1/app/event/{event_uuid}/change_to_win')
    assert response.status_code == 200
    assert response.json()['state'] == EventState.FINISHED_WIN

    async with AsyncClient(app=app, base_url='http://localhost') as ac:
        response = await ac.post(f'/v1/app/event/{event_uuid}/change_to_lose')
    assert response.status_code == 200
    assert response.json()['state'] == EventState.FINISHED_LOSE
