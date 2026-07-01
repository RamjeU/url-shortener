import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.database import DB_PATH


@pytest.fixture
def client():
    if DB_PATH.exists():
        DB_PATH.unlink()

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    if DB_PATH.exists():
        DB_PATH.unlink()


def test_shorten_valid_url(client):
    response = client.post("/api/shorten", json={"url": "https://www.example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert data["original_url"] == "https://www.example.com"


def test_shorten_missing_url(client):
    response = client.post("/api/shorten", json={})
    assert response.status_code == 400


def test_shorten_invalid_url(client):
    response = client.post("/api/shorten", json={"url": "not-a-url"})
    assert response.status_code == 400


def test_redirect_to_original(client):
    post_response = client.post("/api/shorten", json={"url": "https://www.example.com"})
    short_code = post_response.get_json()["short_code"]

    get_response = client.get(f"/{short_code}", follow_redirects=False)
    assert get_response.status_code == 302
    assert get_response.location == "https://www.example.com"


def test_redirect_not_found(client):
    response = client.get("/doesnotexist")
    assert response.status_code == 404


def test_stats_tracks_clicks(client):
    post_response = client.post("/api/shorten", json={"url": "https://www.example.com"})
    short_code = post_response.get_json()["short_code"]

    client.get(f"/{short_code}")
    client.get(f"/{short_code}")

    stats_response = client.get(f"/api/stats/{short_code}")
    data = stats_response.get_json()
    assert data["clicks"] == 2


def test_custom_code(client):
    response = client.post(
        "/api/shorten",
        json={"url": "https://www.example.com", "custom_code": "my-link"},
    )
    assert response.status_code == 201
    assert response.get_json()["short_code"] == "my-link"


def test_custom_code_conflict(client):
    client.post(
        "/api/shorten",
        json={"url": "https://www.example.com", "custom_code": "taken"},
    )
    response = client.post(
        "/api/shorten",
        json={"url": "https://www.other.com", "custom_code": "taken"},
    )
    assert response.status_code == 409
