import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.routes.user import router as user_router
from app.db.models.user import User as UserModel
from app.db.database import get_db

app = FastAPI()
app.include_router(user_router)

# # Fixture for mocked DB session
# @pytest.fixture
# def mock_db():
#     mock_session = AsyncMock(spec=AsyncSession)

#     # Mock the DB response for select(UserModel)
#     mock_result = MagicMock()
#     mock_result.scalars.return_value.all.return_value = [
#         UserModel(id=1, name="Alice", email="alice@example.com"),
#         UserModel(id=2, name="Bob", email="bob@example.com"),
#     ]
#     mock_session.execute.return_value = mock_result

#     return mock_session


# client = TestClient(app)

# def test_create_user():
#     response = client.post("/users", json={"name": "Alice", "age": 25, "email": "alice.li@tom.com"})
#     assert response.status_code == 200
#     data = response.json()
#     assert data["user"]["name"] == "Alice"
#     assert data["user"]["userid"] >= 101

# def test_create_duplicate_user():
#     client.post("/users", json={"name": "Bob", "age": 30, "email": "yonglin.li@tom.com"})
#     response = client.post("/users", json={"name": "Bob", "age": 30, "email": "bob.li@tom.com"})
#     assert response.status_code == 400
#     assert "User already exists" in response.json()["detail"]

# # The test
# @pytest.mark.asyncio
# async def test_get_users(mock_db):
#     # Override the dependency
#     async def override_get_db():
#         yield mock_db
#     app.dependency_overrides[get_db] = override_get_db

#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as ac:
#         response = await ac.get("/users")

#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == 2
#     assert data[0]["name"] == "Alice"
#     assert data[1]["email"] == "bob@example.com"

#     # Cleanup override
#     app.dependency_overrides.clear()


# def test_get_user_success():
#     client.post("/users", json={"name": "Charlie", "age": 22, "email": "charlie.li@tom.com"})
#     response = client.get("/users/103")  # Adjust this if needed
#     assert response.status_code == 200
#     assert "user" in response.json()

# def test_get_user_not_found():
#     response = client.get("/users/999")
#     assert response.status_code == 404

# def test_update_user():
#     client.post("/users", json={"name": "Diana", "age": 28, "email": "yonglin.li@tom.com"})
#     response = client.put("/users/104", json={"name": "Diana Updated", "age": 29, "email": "yonglin.li@tom.com"})
#     assert response.status_code == 200
#     assert response.json()["user"]["name"] == "Diana Updated"

# def test_delete_user():
#     client.post("/users", json={"name": "Eve", "age": 31, "email": "yonglin.li@tom.com"})
#     response = client.delete("/users/105")
#     assert response.status_code == 200
#     assert response.json()["message"] == "User removed"

# def test_delete_user_not_found():
#     response = client.delete("/users/999")
#     assert response.status_code == 404

