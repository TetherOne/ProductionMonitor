import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from unittest.mock import AsyncMock

from src.production_monitor.api.shift_task import crud
from src.production_monitor.api.shift_task.schemas import ShiftTaskSchema


@pytest.mark.asyncio
async def test_get_shift_tasks(
    app_with_mocked_db,
    shift_task_schema,
):
    app, _ = app_with_mocked_db
    crud.get_shift_tasks = AsyncMock(return_value=[shift_task_schema])

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/shift-tasks/", params={"is_closed": False})

    assert response.status_code == 200
    assert response.json()[0]["task_representation"] == "Task A"


@pytest.mark.asyncio
async def test_get_shift_task_by_id(
    app_with_mocked_db,
    monkeypatch,
    shift_task_schema,
):
    app, _ = app_with_mocked_db
    monkeypatch.setattr(
        "src.production_monitor.api.shift_task.crud.get_shift_task_by_id",
        AsyncMock(return_value=shift_task_schema),
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/shift-tasks/1/")

    assert response.status_code == 200
    assert response.json()["task_representation"] == "Task A"


@pytest.mark.asyncio
async def test_create_shift_tasks(
    app_with_mocked_db,
    shift_task_payload,
):
    app, _ = app_with_mocked_db
    crud.create_shift_tasks = AsyncMock(return_value=shift_task_payload)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/api/shift-tasks/create/", json=shift_task_payload)

    assert response.status_code == 201
    assert response.json() == shift_task_payload


@pytest.mark.asyncio
async def test_update_shift_task(
    app_with_mocked_db,
    shift_task_schema,
    shift_task_update_data,
):
    app, _ = app_with_mocked_db

    updated_task = ShiftTaskSchema(
        **{**shift_task_schema.model_dump(), **shift_task_update_data}
    )

    crud.get_shift_task_by_id = AsyncMock(return_value=shift_task_schema)
    crud.update_shift_task = AsyncMock(return_value=updated_task)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.patch(
            "/api/shift-tasks/1/update/", json=shift_task_update_data
        )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["task_representation"] == "Task B"
    assert json_data["is_closed"] is True
    assert json_data["closed_at"] is not None
