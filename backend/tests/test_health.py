from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_check_returns_ok() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"

