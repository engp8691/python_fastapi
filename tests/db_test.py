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
    return mock_session

# Create a user test
@pytest.mark.asyncio
async def test_create_user(mock_db):
    # Mock result of db.execute to simulate no existing user
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    # Mock add to just hold the object
    def add(user):
        user.id = 3  # Simulate DB assigning an ID
    mock_db.add.side_effect = add

    # Mock refresh as noop (id already set above)
    mock_db.refresh = AsyncMock()

    # Mock commit
    mock_db.commit = AsyncMock()

    # Override dependency
    async def override_get_db():
        yield mock_db
    app.dependency_overrides[get_db] = override_get_db

    # Send request
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users", json={
            "name": "Charlie",
            "email": "charlie@example.com",
            "age": 30,
            "role": "user",
            "hashed_password": "eyJhb...64"
        })

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Charlie"
    assert data["email"] == "charlie@example.com"
    assert data["role"] == "user"
    assert data["hashed_password"] == "eyJhb...64"
    
    app.dependency_overrides.clear()

# Get all users test
@pytest.mark.asyncio
async def test_get_users(mock_db):
    # Mock the DB response for select(UserModel)
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        UserModel(id=1, name="Alice", email="alice@example.com"),
        UserModel(id=2, name="Bob", email="bob@example.com"),
    ]
    mock_db.execute.return_value = mock_result

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


@pytest.mark.asyncio
async def test_get_user(mock_db):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = UserModel(id=3, name="Charlie", email="charlie@example.com", age=30)
    mock_db.execute.return_value = mock_result

    # Override the dependency
    async def override_get_db():
        yield mock_db
    app.dependency_overrides[get_db] = override_get_db

    # Send request
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users/3")

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Charlie"
    assert data["email"] == "charlie@example.com"
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_delete_user(mock_db):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = UserModel(id=3, name="Charlie", email="charlie@example.com", age=30)
    mock_db.execute.return_value = mock_result

    # Mock delete
    mock_db.delete = AsyncMock()
    # Mock commit
    mock_db.commit = AsyncMock()

    # Override the dependency
    async def override_get_db():
        yield mock_db
    app.dependency_overrides[get_db] = override_get_db

    # Send request
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/users/3")

    data = response.json()

    assert response.status_code == 200
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_update_user(mock_db):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = UserModel(id=3, name="Old_Charlie", email="old_charlie@example.com", age=30)
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
        response = await ac.put("/users/3", json={
            "name": "New_Charlie",
            "age": 35,
            "email": "new_charlie@tom.com",
            "role": "user",
            "hashed_password": "eyJhb...64"
        })

    data = response.json()

    assert response.status_code == 200
    assert data["user"]["name"] == "New_Charlie"
    assert data["user"]["email"] == "new_charlie@tom.com"
    assert data["user"]["age"] == 35
    assert data["user"]["role"] == "user"
    assert data["user"]["hashed_password"] == "eyJhb...64"
    
    app.dependency_overrides.clear()
