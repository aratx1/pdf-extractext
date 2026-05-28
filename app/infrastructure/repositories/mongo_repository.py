from datetime import datetime, timezone
from uuid import UUID, uuid4
from motor.motor_asyncio import AsyncIOMotorClient
from app.application.interfaces.summary_repository import Summary, SummaryRepository
from app.core import get_settings


class MongoSummaryRepository(SummaryRepository):
    def __init__(self, mongodb_url: str | None = None, db_name: str | None = None):
        settings = get_settings()
        self._client = AsyncIOMotorClient(mongodb_url or settings.mongodb_url)
        self._db = self._client[db_name or settings.mongodb_db_name]
        self._collection = self._db.summaries

    async def save(self, summary: Summary) -> Summary:
        summary.id = uuid4()
        summary.created_at = datetime.now(timezone.utc)

        doc = {
            "_id": str(summary.id),
            "original_filename": summary.original_filename,
            "summary_text": summary.summary_text,
            "extracted_text": summary.extracted_text,
            "created_at": summary.created_at.isoformat(),
        }
        await self._collection.insert_one(doc)
        return summary

    async def get_by_id(self, summary_id: UUID) -> Summary | None:
        doc = await self._collection.find_one({"_id": str(summary_id)})
        if doc is None:
            return None
        return self._doc_to_summary(doc)

    async def get_all(self, limit: int = 100) -> list[Summary]:
        cursor = self._collection.find().sort("created_at", -1).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [self._doc_to_summary(doc) for doc in docs]

    def _doc_to_summary(self, doc: dict) -> Summary:
        return Summary(
            id=UUID(doc["_id"]),
            original_filename=doc["original_filename"],
            summary_text=doc["summary_text"],
            extracted_text=doc.get("extracted_text", ""),
            created_at=datetime.fromisoformat(doc["created_at"]),
        )
