import pytest
from unittest.mock import AsyncMock

from src.production_monitor.main import app


@pytest.fixture
def app_with_mocked_db():
    mocked_session = AsyncMock()
    return app, mocked_session
