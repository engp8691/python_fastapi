from datetime import datetime, timedelta, timezone
import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock
from jose import jwt
from app.routes.user import router as user_router
from app.db.models.orm_models import UserModelDB
from app.db.database import get_db
from app.utils.token import ALGORITHM, SECRET_KEY

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
        user.id = 'cfee03779e32418882389be25762c2af'
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
            "password": "password-fake"
        })

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Charlie"
    assert data["email"] == "charlie@example.com"
    assert data["role"] == "user"
    
    app.dependency_overrides.clear()

# Get all users test
@pytest.mark.asyncio
async def test_get_users(mock_db):
    # Mock the return in file `app/utils/token.py` at line 61
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = UserModelDB(id=3, name="Charlie", role="administrator", email="charlie@example.com", age=30)
    mock_db.execute.return_value = mock_result

    # Mock the return in file `app/routes/user.py` at line 56
    mock_result.scalars.return_value.all.return_value = [
        UserModelDB(id='cfee03779e32418882389be25762c2af', name="Alice", email="alice@example.com", role="administrator", age=30),
        UserModelDB(id='cfee03779e32418882389be25762c2af', name="Bob", email="bob@example.com", role="user", age=20),
    ]
    mock_db.execute.return_value = mock_result

    # Override the dependency
    async def override_get_db():
        yield mock_db
    app.dependency_overrides[get_db] = override_get_db

    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {
        "sub": "1",
        "user": {
            "name": "nobody",
            "role": "administrator",
            "age": 25,
            "email": "nobody@tom.com"
        },
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    headers = {
       "Authorization":  f"Bearer {encoded_jwt}"
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users", headers=headers)

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
    mock_result.scalars.return_value.first.return_value = UserModelDB(id='cfee03779e32418882389be25762c2af', name="Charlie", email="charlie@example.com", age=30, role="user")
    mock_db.execute.return_value = mock_result

    # Override the dependency
    async def override_get_db():
        yield mock_db
    app.dependency_overrides[get_db] = override_get_db

    # Send request
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users/cfee03779e32418882389be25762c2af")

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Charlie"
    assert data["email"] == "charlie@example.com"
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_delete_user(mock_db):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = UserModelDB(id='cfee03779e32418882389be25762c2af', name="Charlie", email="charlie@example.com", age=30)
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
        response = await ac.delete("/users/cfee03779e32418882389be25762c2af")

    data = response.json()

    assert response.status_code == 200
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_update_user(mock_db):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = UserModelDB(id='cfee03779e32418882389be25762c2af', name="Old_Charlie", email="old_charlie@example.com", age=30)
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
            "password": "new_password"
        })

    data = response.json()

    assert response.status_code == 200
    assert data["user"]["name"] == "New_Charlie"
    assert data["user"]["email"] == "new_charlie@tom.com"
    assert data["user"]["age"] == 35
    assert data["user"]["role"] == "user"
    
    app.dependency_overrides.clear()
