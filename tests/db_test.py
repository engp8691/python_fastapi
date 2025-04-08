import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock

from app.routes.user import router as user_router
from app.db.models.user import User as UserModel
from app.db.database import get_db

# Create test app and add routes
app = FastAPI()
app.include_router(user_router)

# Fixture for mocked DB session
@pytest.fixture
def mock_db():
    mock_session = AsyncMock(spec=AsyncSession)

    # Mock the DB response for select(UserModel)
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        UserModel(id=1, name="Alice", email="alice@example.com"),
        UserModel(id=2, name="Bob", email="bob@example.com"),
    ]
    mock_session.execute.return_value = mock_result

    return mock_session

# The test
@pytest.mark.asyncio
async def test_get_users(mock_db):
    # Override the dependency
    async def override_get_db():
        yield mock_db
    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["email"] == "bob@example.com"

    # Cleanup override
    app.dependency_overrides.clear()
