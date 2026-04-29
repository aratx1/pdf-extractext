from dataclasses import replace
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.interfaces.ai_provider import AIResponse
from app.application.interfaces.summary_repository import Summary
from app.application.services.pdf_service import ExtractedPDF
from app.application.services.summary_service import SummaryService


class StubPDFService:
    def __init__(self, extracted: ExtractedPDF):
        self.extracted = extracted
        self.calls = []

    def extract_text(self, file_content: bytes, filename: str) -> ExtractedPDF:
        self.calls.append((file_content, filename))
        return self.extracted


class StubAIProvider:
    def __init__(self, response: AIResponse):
        self.response = response
        self.calls = []

    async def generate_summary(self, text: str, max_length: int = 500) -> AIResponse:
        self.calls.append((text, max_length))
        return self.response

    async def health_check(self) -> bool:
        return True


class StubRepository:
    def __init__(self, stored: Summary):
        self.stored = stored
        self.saved = None

    async def save(self, summary: Summary) -> Summary:
        self.saved = summary
        return replace(
            self.stored,
            original_filename=summary.original_filename,
            summary_text=summary.summary_text,
            extracted_text=summary.extracted_text,
        )

    async def get_by_id(self, summary_id):
        return self.stored if self.stored.id == summary_id else None

    async def get_all(self, limit: int = 100):
        return [self.stored][:limit]


@pytest.mark.asyncio
async def test_create_summary_orchestrates_pdf_ai_and_repository():
    extracted_text = "A" * 1200
    extracted = ExtractedPDF(
        filename="paper.pdf",
        text=extracted_text,
        page_count=4,
        character_count=len(extracted_text),
    )
    stored_summary = Summary(
        id=uuid4(),
        original_filename="paper.pdf",
        summary_text="Stored summary",
        extracted_text="",
        created_at=datetime.now(timezone.utc),
    )
    pdf_service = StubPDFService(extracted)
    ai_provider = StubAIProvider(
        AIResponse(content="Short summary", model="test-model", tokens_used=42)
    )
    repository = StubRepository(stored_summary)
    service = SummaryService(pdf_service, ai_provider, repository)

    result = await service.create_summary(b"pdf-bytes", "paper.pdf")

    assert pdf_service.calls == [(b"pdf-bytes", "paper.pdf")]
    assert ai_provider.calls == [(extracted_text, 500)]
    assert repository.saved is not None
    assert repository.saved.original_filename == "paper.pdf"
    assert repository.saved.summary_text == "Short summary"
    assert repository.saved.extracted_text == extracted_text[:1000]
    assert result.id == stored_summary.id
    assert result.summary_text == "Short summary"


@pytest.mark.asyncio
async def test_get_summary_and_list_summaries_delegate_to_repository():
    stored_summary = Summary(
        id=uuid4(),
        original_filename="paper.pdf",
        summary_text="Stored summary",
        extracted_text="Extracted",
        created_at=datetime.now(timezone.utc),
    )
    service = SummaryService(
        StubPDFService(
            ExtractedPDF(
                filename="paper.pdf",
                text="ignored",
                page_count=1,
                character_count=7,
            )
        ),
        StubAIProvider(AIResponse(content="ignored", model="test-model")),
        StubRepository(stored_summary),
    )

    fetched = await service.get_summary(stored_summary.id)
    listed = await service.list_summaries(limit=10)

    assert fetched == stored_summary
    assert listed == [stored_summary]
