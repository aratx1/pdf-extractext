from datetime import datetime, timedelta, timezone

import pytest

from app.application.interfaces.summary_repository import Summary
from app.infrastructure.repositories.in_memory_repository import (
    InMemorySummaryRepository,
)


@pytest.mark.asyncio
async def test_save_assigns_id_and_created_at():
    repository = InMemorySummaryRepository()
    summary = Summary(
        id=None,
        original_filename="test.pdf",
        summary_text="Summary",
        extracted_text="Extracted",
        created_at=None,
    )

    saved = await repository.save(summary)

    assert saved.id is not None
    assert saved.created_at is not None


@pytest.mark.asyncio
async def test_get_all_returns_newest_first_and_honors_limit():
    repository = InMemorySummaryRepository()
    older = Summary(
        id=None,
        original_filename="old.pdf",
        summary_text="Old",
        extracted_text="Old text",
        created_at=None,
    )
    newer = Summary(
        id=None,
        original_filename="new.pdf",
        summary_text="New",
        extracted_text="New text",
        created_at=None,
    )

    saved_older = await repository.save(older)
    saved_newer = await repository.save(newer)
    saved_older.created_at = datetime.now(timezone.utc) - timedelta(days=1)
    saved_newer.created_at = datetime.now(timezone.utc)

    results = await repository.get_all(limit=1)

    assert results == [saved_newer]
    assert results[0].original_filename == "new.pdf"
