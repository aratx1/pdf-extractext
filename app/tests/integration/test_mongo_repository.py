"""Integration tests for MongoSummaryRepository with Docker-based MongoDB."""

import pytest
from datetime import datetime, timezone

from uuid import UUID

from app.application.interfaces.summary_repository import Summary


@pytest.mark.integration
@pytest.mark.asyncio
async def test_save_assigns_id_and_created_at(mongo_repository, sample_summary):
    saved = await mongo_repository.save(sample_summary)

    assert saved.id is not None
    assert saved.created_at is not None
    assert saved.original_filename == "test.pdf"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_by_id_returns_saved_summary(mongo_repository, sample_summary):
    saved = await mongo_repository.save(sample_summary)

    fetched = await mongo_repository.get_by_id(saved.id)

    assert fetched is not None
    assert fetched.id == saved.id
    assert fetched.summary_text == saved.summary_text
    assert fetched.extracted_text == saved.extracted_text


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_unknown(mongo_repository):
    result = await mongo_repository.get_by_id(UUID("00000000-0000-0000-0000-000000000000"))

    assert result is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_all_returns_newest_first(mongo_repository):
    older = Summary(
        id=None,
        original_filename="old.pdf",
        summary_text="Old summary",
        extracted_text="Old text",
        created_at=datetime.now(timezone.utc).replace(year=2020),
    )
    newer = Summary(
        id=None,
        original_filename="new.pdf",
        summary_text="New summary",
        extracted_text="New text",
        created_at=None,
    )

    saved_older = await mongo_repository.save(older)
    saved_newer = await mongo_repository.save(newer)

    saved_older.created_at = datetime.now(timezone.utc).replace(year=2020)
    await mongo_repository._collection.update_one(
        {"_id": saved_older.id}, {"$set": {"created_at": saved_older.created_at}}
    )

    results = await mongo_repository.get_all(limit=10)

    assert len(results) == 2
    assert results[0].original_filename == "new.pdf"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_all_honors_limit(mongo_repository):
    for i in range(5):
        await mongo_repository.save(
            Summary(
                id=None,
                original_filename=f"doc_{i}.pdf",
                summary_text=f"Summary {i}",
                extracted_text=f"Text {i}",
                created_at=None,
            )
        )

    results = await mongo_repository.get_all(limit=2)

    assert len(results) == 2


@pytest.mark.integration
@pytest.mark.asyncio
async def test_save_updates_existing_summary(mongo_repository, sample_summary):
    saved = await mongo_repository.save(sample_summary)

    saved.summary_text = "Updated summary text"
    updated = await mongo_repository.save(saved)

    fetched = await mongo_repository.get_by_id(saved.id)

    assert fetched.summary_text == "Updated summary text"
    assert fetched.id == saved.id
