from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.application.interfaces.summary_repository import Summary
from app.main import app
from app.presentation.routers.pdf_summary import get_summary_service


class StubSummaryService:
    def __init__(self):
        self.created = []
        self.summaries = [
            Summary(
                id=uuid4(),
                original_filename="stored.pdf",
                summary_text="Stored summary",
                extracted_text="Stored extracted",
                created_at=datetime.now(timezone.utc),
            )
        ]

    async def create_summary(self, file_content: bytes, filename: str) -> Summary:
        self.created.append((file_content, filename))
        if filename == "invalid.pdf":
            raise ValueError("Invalid PDF")

        return Summary(
            id=uuid4(),
            original_filename=filename,
            summary_text="Generated summary",
            extracted_text="Extracted",
            created_at=datetime.now(timezone.utc),
        )

    async def get_summary(self, summary_id):
        for summary in self.summaries:
            if summary.id == summary_id:
                return summary
        return None

    async def list_summaries(self, limit: int = 100):
        return self.summaries[:limit]

    async def health_check(self):
        return True

    @property
    def _ai_provider(self):
        return self


def test_summarize_pdf_returns_summary_for_valid_upload():
    service = StubSummaryService()
    app.dependency_overrides[get_summary_service] = lambda: service

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/summarize",
                files={"file": ("report.pdf", b"%PDF-1.4", "application/pdf")},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["original_filename"] == "report.pdf"
    assert data["summary_text"] == "Generated summary"
    assert service.created == [(b"%PDF-1.4", "report.pdf")]


def test_summarize_pdf_rejects_non_pdf_upload():
    service = StubSummaryService()
    app.dependency_overrides[get_summary_service] = lambda: service

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/summarize",
                files={"file": ("notes.txt", b"text", "text/plain")},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json() == {"detail": "Only PDF files are supported"}


def test_summarize_pdf_rejects_empty_file():
    service = StubSummaryService()
    app.dependency_overrides[get_summary_service] = lambda: service

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/summarize",
                files={"file": ("empty.pdf", b"", "application/pdf")},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json() == {"detail": "Empty file uploaded"}


def test_summarize_pdf_returns_bad_request_for_invalid_pdf():
    service = StubSummaryService()
    app.dependency_overrides[get_summary_service] = lambda: service

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/summarize",
                files={"file": ("invalid.pdf", b"broken", "application/pdf")},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid PDF"}


def test_list_summaries_returns_serialized_items():
    service = StubSummaryService()
    app.dependency_overrides[get_summary_service] = lambda: service

    try:
        with TestClient(app) as client:
            response = client.get("/api/summaries?limit=10")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["summaries"][0]["original_filename"] == "stored.pdf"


def test_get_summary_returns_not_found_for_unknown_id():
    service = StubSummaryService()
    app.dependency_overrides[get_summary_service] = lambda: service

    try:
        with TestClient(app) as client:
            response = client.get(f"/api/summaries/{uuid4()}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {"detail": "Summary not found"}
