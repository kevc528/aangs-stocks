from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app

client = TestClient(app)

def test_redirect_not_logged_in():
    response = client.post(
        "/stock",
        json={"ticker": "AMZN", "mode": "buy", "price": 123.32}
    )

    assert response.status_code >= 300 and response.status_code < 400

def test_register_user(mocker):
    mocker.patch.object(Session, "add", autospec=True)
    mocker.patch.object(Session, "commit", autospec=True)
    mocker.patch.object(Session, "refresh", autospec=True)

    response = client.post(
        "/user",
        json={"email": "aang@gmail.com", "password": "password"},
    )

    assert response.status_code == 200

def test_register_user_bad_schema(mocker):
    mocker.patch.object(Session, "add", autospec=True)
    mocker.patch.object(Session, "commit", autospec=True)
    mocker.patch.object(Session, "refresh", autospec=True)

    response = client.post(
        "/user",
        json={"password": "password"},
    )

    assert response.status_code != 200

