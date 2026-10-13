
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "AI Document Assistant API is running"
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_ask_endpoint_missing_question():
    response = client.post("/ask", json={})

    assert response.status_code == 422
