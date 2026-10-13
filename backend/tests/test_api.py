import os
import pymupdf
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

def test_upload_pdf_rejects_corrupted_file():
    response = client.post(
        "/upload-pdf",
        files={
            "file": (
                "corrupted.pdf",
                b"This is not valid PDF content.",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Could not process this PDF file"
    }


def test_upload_pdf_extracts_text():
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "Hello from automated testing")

    pdf_bytes = document.tobytes()
    document.close()

    response = client.post(
        "/upload-pdf",
        files={
            "file": (
                "sample.pdf",
                pdf_bytes,
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["filename"] == "sample.pdf"
    assert data["pages"] == 1
    assert data["characters_extracted"] > 0
    assert "Hello from automated testing" in data["text"]

def test_upload_pdf_rejects_pdf_without_text():
    document = pymupdf.open()
    document.new_page()

    pdf_bytes = document.tobytes()
    document.close()

    response = client.post(
        "/upload-pdf",
        files={
            "file": (
                "blank.pdf",
                pdf_bytes,
                "application/pdf",
            )
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "No extractable text found. The PDF may be scanned."
    }

def test_ask_pdf_rejects_non_pdf_file(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    response = client.post(
        "/ask-pdf",
        data={"question": "What is this document about?"},
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

def test_ask_pdf_rejects_empty_file(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    response = client.post(
        "/ask-pdf",
        data={"question": "What is in this document?"},
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
