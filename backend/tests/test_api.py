
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

def test_upload_pdf_rejects_non_pdf_file():
    response = client.post(
        "/upload-pdf",
        files={
            "file": (
                "document.txt",
                b"This is not a PDF file.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Please upload a PDF file"
    }

def test_upload_pdf_rejects_empty_file():
    response = client.post(
        "/upload-pdf",
        files={
            "file": (
                "empty.pdf",
                b"",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The uploaded PDF is empty"
    }
