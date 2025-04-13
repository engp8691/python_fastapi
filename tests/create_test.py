import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock

from app.routes.user import router as user_router
from app.db.models.user import UserModelDB
from app.db.database import get_db

# Create test app
app = FastAPI()
app.include_router(user_router)

# Fixture for mocked DB session
@pytest.fixture
def mock_db():
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session

@pytest.mark.asyncio
async def test_update_user(mock_db):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = UserModelDB(id='cfee03779e32418882389be25762c2af', name="Old_Charlie", email="old_charlie@example.com", role="user", age=30)
    mock_db.execute.return_value = mock_result

    # Mock commit
    mock_db.commit.return_value = None
    # Mock update
    mock_db.refresh = AsyncMock()
    
    # Override the dependency
    async def override_get_db():
        yield mock_db
    app.dependency_overrides[get_db] = override_get_db

    # Send request
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/users/cfee03779e32418882389be25762c2af", json={
            "name": "New_Charlie",
            "age": 35,
            "email": "new_charlie@tom.com",
            "role": "user",
            "password": "fake-password"
        })

    data = response.json()

    assert response.status_code == 200
    assert data["user"]["name"] == "New_Charlie"
    assert data["user"]["email"] == "new_charlie@tom.com"
    assert data["user"]["age"] == 35
    assert data["user"]["role"] == "user"
    
    app.dependency_overrides.clear()
