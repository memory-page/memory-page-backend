from httpx import AsyncClient, ASGITransport
from fastapi import status
import pytest

from app.main import app


@pytest.mark.asyncio
async def test_main() -> None:
    # Given
    mock_response = {"I'm ready": "OK"}

    # When
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_response
