import pytest
import yaml
from werkzeug.security import generate_password_hash

from tiefkuehlliste import create_app


@pytest.fixture
def app(tmp_path):
    users = tmp_path / "users.yaml"
    users.write_text(
        yaml.safe_dump(
            {"users": [{"username": "anna", "password_hash": generate_password_hash("secret")}]},
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test",
            "DATABASE": str(tmp_path / "test.sqlite"),
            "USERS_FILE": str(users),
        }
    )


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    client.get("/login")
    with client.session_transaction() as s:
        token = s["csrf_token"]
    response = client.post(
        "/login", data={"username": "anna", "password": "secret", "csrf_token": token}
    )
    assert response.status_code == 302
    with client.session_transaction() as s:
        token = s["csrf_token"]
    return {"X-CSRF-Token": token}
