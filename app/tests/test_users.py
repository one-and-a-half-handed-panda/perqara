from accessors.users import Base
from database import get_db_session
from fastapi.testclient import TestClient
from main import app
from models.responses import is_valid_timestamp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db_session] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/",
        json={"user_name": "deadpool", "user_age": 500},
    )
    data = response.json()["data"]
    assert response.status_code == 200, response.text
    assert data["user_name"] == "deadpool"
    assert "user_id" in data

    user_id = data["user_id"]

    response = client.get(f"/users/{user_id}")
    data = response.json()["data"]
    assert response.status_code == 200, response.text
    assert data["user_name"] == "deadpool"
    assert data["user_age"] == 500
    assert data["user_id"] == user_id


def test_create_user_expect_assertion_error_user_age():
    response = client.post(
        "/users/",
        json={"user_name": "deadpool", "user_age": 0},
    )
    data = response.json()["detail"][0]
    assert response.status_code == 422, response.text
    assert data["msg"] == "Assertion failed, The user must be at least 17 years old!"


def test_create_user_expect_assertion_error_user_name():
    response = client.post(
        "/users/",
        json={"user_name": "", "user_age": 500},
    )
    data = response.json()["detail"][0]
    assert response.status_code == 422, response.text
    assert data["msg"] == "Assertion failed, user_name must be a string of at least 2 letters"


def test_update_user():
    response = client.get(
        "/users/",
    )
    data = response.json()["data"]
    assert response.status_code == 200, response.text
    assert len(data) > 0

    user_id = data[0]["user_id"]
    user_name = "mr pa"
    user_age = 50

    response = client.put(
        f"/users/{user_id}",
        json={"user_id": user_id, "user_name": user_name, "user_age": user_age},
    )
    data = response.json()["data"]
    assert response.status_code == 200, response.text

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["user_name"] == user_name
    assert data["user_age"] == user_age
    assert data["user_id"] == user_id


def test_update_user_expect_assertion_error_user_age():
    response = client.get(
        "/users/",
    )
    data = response.json()["data"]
    assert response.status_code == 200, response.text
    assert len(data) > 0

    user_id = data[0]["user_id"]
    user_age = 0
    user_name = data[0]["user_name"]

    response = client.put(
        f"/users/{user_id}",
        json={"user_id": user_id, "user_name": user_name, "user_age": user_age},
    )
    data = response.json()["detail"][0]
    assert response.status_code == 422, response.text
    assert data["msg"] == "Assertion failed, The user must be at least 17 years old!"


def test_update_user_expect_assertion_error_user_name():
    response = client.get(
        "/users/",
    )
    data = response.json()["data"]
    assert response.status_code == 200, response.text
    assert len(data) > 0

    user_id = data[0]["user_id"]
    user_age = data[0]["user_age"]
    user_name = ""

    response = client.put(
        f"/users/{user_id}",
        json={"user_id": user_id, "user_name": user_name, "user_age": user_age},
    )
    data = response.json()["detail"][0]
    assert response.status_code == 422, response.text
    assert data["msg"] == "Assertion failed, user_name must be a string of at least 2 letters"


def test_update_user_expect_user_not_found_exception():
    response = client.post(
        "/users/",
        json={"user_name": "deadpool", "user_age": 500},
    )
    data = response.json()["data"]
    assert response.status_code == 200, response.text
    assert data["user_name"] == "deadpool"
    assert "user_id" in data

    user_id = data["user_id"]

    response = client.delete(
        f"/users/{user_id}",
    )
    data = response.json()["data"]
    assert response.status_code == 200, response.text
    assert data["user_id"] == user_id

    user_name = "mr pa"
    user_age = 50

    response = client.put(
        f"/users/{user_id}",
        json={"user_id": user_id, "user_name": user_name, "user_age": user_age},
    )
    data = response.json()
    assert response.status_code == 404, response.text
    assert data["code"] == "404"
    assert data["message"] == "User not found!"
    assert is_valid_timestamp(data["timestamp"])


def test_delete_user():
    response = client.post(
        "/users/",
        json={"user_name": "deadpool", "user_age": 500},
    )
    data = response.json()["data"]
    assert response.status_code == 200, response.text
    assert data["user_name"] == "deadpool"
    assert "user_id" in data

    user_id = data["user_id"]

    response = client.delete(
        f"/users/{user_id}",
    )
    data = response.json()["data"]
    assert response.status_code == 200, response.text
    assert data["user_id"] == user_id

    response = client.get(f"/users/{user_id}")
    data = response.json()
    assert response.status_code == 404, response.text
    assert data["code"] == "404"
    assert data["message"] == "User not found!"
    assert is_valid_timestamp(data["timestamp"])
