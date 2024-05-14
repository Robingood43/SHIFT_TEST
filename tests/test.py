import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from SHIFT import init_routers
from SHIFT.app.controller.crud.user.user import check_password
from SHIFT.app.model import User, DatabaseUserGateway, SalaryDetails


class MockDatabase(DatabaseUserGateway):
    async def get_user_by_id_and_email(self, id_, username) -> Optional[User]:
        if id_ == 1 and username == 'user@example.com':
            return User(
                id=1, username="user@example.com", hashed_password="$2b$12$nhEYfC7pRyS.KGZezH7htO5XAj1pg8k/sgJGdYcY6boH2SH1nn4y2"
            )
        elif id_ == 2 and username == 'user2@example.com':
            return User(
                id=2, username="user@example.com", hashed_password="$2b$12$nhEYfC7pRyS.KGZezH7htO5XAj1pg8k/sgJGdYcY6boH2SH1nn4y2"
            )

    async def get_user_by_email_and_password(self, username: str, password: str) -> Optional[User]:
        if username == "user@example.com" and check_password(
                password, "$2b$12$nhEYfC7pRyS.KGZezH7htO5XAj1pg8k/sgJGdYcY6boH2SH1nn4y2"
        ):
            return User(
                id=1, username="user@example.com", hashed_password="$2b$12$nhEYfC7pRyS.KGZezH7htO5XAj1pg8k/sgJGdYcY6boH2SH1nn4y2"
            )
        elif username == "user2@example.com" and check_password(
                password, "$2b$12$nhEYfC7pRyS.KGZezH7htO5XAj1pg8k/sgJGdYcY6boH2SH1nn4y2"
        ):
            return User(
                id=2, username="user2@example.com", hashed_password="$2b$12$nhEYfC7pRyS.KGZezH7htO5XAj1pg8k/sgJGdYcY6boH2SH1nn4y2"
            )

    async def get_salary_details(self, id_: int) -> Optional[SalaryDetails]:
        if id_ == 1:
            return SalaryDetails(
                id=1, salary=10000.00, next_raise=datetime.datetime.now().date()
            )


@fixture
def client():
    app = FastAPI()
    init_routers(app)
    app.dependency_overrides[DatabaseUserGateway] = MockDatabase
    return TestClient(app)


def test_login(client):
    response = client.post("/login", data={"username": "user@example.com", "password": "string"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    response = client.post("/login", data={"username": "user2@example.com", "password": "string"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_error_login(client):
    response = client.post("/login", data={"username": "user@example.com", "password": "ERROR"})
    assert response.status_code == 401
    assert "access_token" not in response.json()
    assert "token_type" not in response.json()
    response = client.post("/login", data={"username": "ERROR", "password": "string"})
    assert response.status_code == 401
    assert "access_token" not in response.json()
    assert "token_type" not in response.json()


def test_get_salary(client):
    response = client.post("/login", data={"username": "user@example.com", "password": "string"})
    access_token = response.json()["access_token"]

    response = client.get("/salary", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "salary" in response.json()
    assert "next_raise_date" in response.json()

    response = client.post("/login", data={"username": "user2@example.com", "password": "string"})
    access_token = response.json()["access_token"]
    response = client.get("/salary", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 404
    assert "salary" not in response.json()
    assert "next_raise_date" not in response.json()


def test_get_salary_invalid_token(client):
    response = client.get("/salary", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
