from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.routes import user as user_routes
from app.types.user import User

app = FastAPI()
app.include_router(user_routes.router)

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={"name": "Alice", "age": 25, "email": "alice.li@tom.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["name"] == "Alice"
    assert data["user"]["userid"] >= 101

def test_create_duplicate_user():
    client.post("/users", json={"name": "Bob", "age": 30, "email": "yonglin.li@tom.com"})
    response = client.post("/users", json={"name": "Bob", "age": 30, "email": "bob.li@tom.com"})
    assert response.status_code == 400
    assert "User already exists" in response.json()["detail"]

def test_get_user_success():
    client.post("/users", json={"name": "Charlie", "age": 22, "email": "charlie.li@tom.com"})
    response = client.get("/users/103")  # Adjust this if needed
    assert response.status_code == 200
    assert "user" in response.json()

def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404

def test_update_user():
    client.post("/users", json={"name": "Diana", "age": 28, "email": "yonglin.li@tom.com"})
    response = client.put("/users/104", json={"name": "Diana Updated", "age": 29, "email": "yonglin.li@tom.com"})
    assert response.status_code == 200
    assert response.json()["user"]["name"] == "Diana Updated"

def test_delete_user():
    client.post("/users", json={"name": "Eve", "age": 31, "email": "yonglin.li@tom.com"})
    response = client.delete("/users/105")
    assert response.status_code == 200
    assert response.json()["message"] == "User removed"

def test_delete_user_not_found():
    response = client.delete("/users/999")
    assert response.status_code == 404
