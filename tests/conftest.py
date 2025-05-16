import pytest
from unittest.mock import AsyncMock

from datetime import datetime, date

from src.production_monitor.api.product_code.schemas import (
    AggregateProductCodeRequest,
    ProductCodeSchema,
    ProductCodeCreateSchema,
)
from src.production_monitor.api.shift_task.schemas import ShiftTaskSchema
from src.production_monitor.main import app
from src.production_monitor.models import ProductCode


@pytest.fixture
def app_with_mocked_db():
    mocked_session = AsyncMock()
    return app, mocked_session


@pytest.fixture
def shift_task_dict():
    return {
        "id": 1,
        "task_representation": "Task A",
        "work_center": "WC1",
        "shift": "Morning",
        "brigade": "Brigade A",
        "batch_number": 101,
        "batch_date": date(2024, 9, 14),
        "nomenclature": "NOM-001",
        "code_ekn": "EK123",
        "rc_identifier": "RC-A",
        "shift_start": datetime(2024, 9, 14, 8, 0),
        "shift_end": datetime(2024, 9, 14, 16, 0),
        "is_closed": False,
        "closed_at": None,
    }


@pytest.fixture
def shift_task_schema(shift_task_dict):
    return ShiftTaskSchema(**shift_task_dict)


@pytest.fixture
def shift_task_payload():
    return [
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


@pytest.fixture
def shift_task_update_data():
    return {
        "task_representation": "Task B",
        "work_center": "WC2",
        "shift": "Evening",
        "brigade": "Brigade B",
        "batch_number": 202,
        "batch_date": date(2025, 5, 15).isoformat(),
        "nomenclature": "NOM-002",
        "code_ekn": "EK456",
        "rc_identifier": "RC-B",
        "shift_start": datetime(2025, 5, 15, 16, 0).isoformat(),
        "shift_end": datetime(2025, 5, 15, 23, 59).isoformat(),
        "is_closed": True,
        "closed_at": datetime(2025, 5, 16, 0, 30).isoformat(),
    }


@pytest.fixture
def product_code_create_data():
    return [
        ProductCodeCreateSchema(
            unique_code="ABC123",
            batch_number=101,
            batch_date=date(2025, 5, 15),
        ),
        ProductCodeCreateSchema(
            unique_code="XYZ789",
            batch_number=102,
            batch_date=date(2025, 5, 15),
        ),
    ]


@pytest.fixture
def product_code_response_data():
    return [
        ProductCodeSchema(
            id=1,
            unique_code="ABC123",
            is_aggregated=False,
            aggregated_at=None,
            shift_task_id=1,
        ),
        ProductCodeSchema(
            id=2,
            unique_code="XYZ789",
            is_aggregated=False,
            aggregated_at=None,
            shift_task_id=1,
        ),
    ]


@pytest.fixture
def aggregate_request_data():
    return AggregateProductCodeRequest(
        shift_task_id=1,
        unique_code="ABC123",
    )


@pytest.fixture
def aggregated_product_code_obj():
    return ProductCode(
        id=1,
        unique_code="ABC123",
        is_aggregated=True,
        aggregated_at=datetime(2025, 5, 16),
        shift_task_id=1,
    )
