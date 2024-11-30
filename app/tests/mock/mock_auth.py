from httpx import AsyncClient, ASGITransport, Response

from app.main import app


async def mock_login(
    board_name: str, 
    password: str
) -> Response:
    
    login_request = {
        "board_name":board_name,
        "password":password
    }
    
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/board/login", json=login_request)
    
    return response
