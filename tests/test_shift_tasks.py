import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from datetime import datetime, date
from unittest.mock import AsyncMock

from src.production_monitor.api.shift_task import crud
from src.production_monitor.api.shift_task.schemas import ShiftTaskSchema


@pytest.mark.asyncio
async def test_get_shift_tasks(app_with_mocked_db):
    app, mocked_session = app_with_mocked_db

    fake_data = [
        ShiftTaskSchema(
            id=1,
            task_representation="Task A",
            work_center="WC1",
            shift="Morning",
            brigade="Brigade A",
            batch_number=101,
            batch_date=date(2024, 9, 14),
            nomenclature="NOM-001",
            code_ekn="EK123",
            rc_identifier="RC-A",
            shift_start=datetime(2024, 9, 14, 8, 0),
            shift_end=datetime(2024, 9, 14, 16, 0),
            is_closed=False,
            closed_at=None,
        )
    ]

    crud.get_shift_tasks = AsyncMock(return_value=fake_data)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/shift-tasks/", params={"is_closed": False})

    assert response.status_code == 200
    assert response.json()[0]["task_representation"] == "Task A"


@pytest.mark.asyncio
async def test_create_shift_tasks(app_with_mocked_db):
    app, mocked_session = app_with_mocked_db

    test_payload = [
        {
            "task_representation": "Task A",
            "work_center": "WC1",
            "shift": "Morning",
            "brigade": "Brigade A",
            "batch_number": 101,
            "batch_date": str(date(2024, 9, 14)),
            "nomenclature": "NOM-001",
            "code_ekn": "EK123",
            "rc_identifier": "RC-A",
            "shift_start": datetime(2024, 9, 14, 8, 0).isoformat(),
            "shift_end": datetime(2024, 9, 14, 16, 0).isoformat(),
            "is_closed": False,
            "closed_at": None,
        }
    ]

    expected_result = test_payload
    crud.create_shift_tasks = AsyncMock(return_value=expected_result)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/api/shift-tasks/create/", json=test_payload)

    assert response.status_code == 201
    assert response.json() == expected_result
