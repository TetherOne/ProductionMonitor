import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_add_product_code(
    app_with_mocked_db,
    product_code_create_data,
    product_code_response_data,
    monkeypatch,
):
    app, mocked_session = app_with_mocked_db

    monkeypatch.setattr(
        "src.production_monitor.api.product_code.crud.add_product_codes",
        AsyncMock(return_value=product_code_response_data),
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/api/product-codes/add/",
            json=jsonable_encoder(product_code_create_data),
        )

    assert response.status_code == 201
    json_data = response.json()
    assert isinstance(json_data, list)
    assert json_data[0]["unique_code"] == "ABC123"
    assert json_data[1]["unique_code"] == "XYZ789"


@pytest.mark.asyncio
async def test_aggregate_product_code(
    app_with_mocked_db,
    aggregate_request_data,
    aggregated_product_code_obj,
    monkeypatch,
):
    app, mocked_session = app_with_mocked_db

    async def fake_validate_product_codes(*args, **kwargs):
        return aggregated_product_code_obj

    monkeypatch.setattr(
        "src.production_monitor.api.product_code.crud.validate_product_codes",
        fake_validate_product_codes,
    )

    async def fake_commit():
        return None

    mocked_session.commit = AsyncMock(side_effect=fake_commit)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/api/product-codes/aggregate/",
            json=aggregate_request_data.model_dump(),
        )

    assert response.status_code == 201
    json_data = response.json()
    assert "unique_code" in json_data
    assert json_data["unique_code"] == "ABC123"
