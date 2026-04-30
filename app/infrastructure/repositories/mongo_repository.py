"""MongoDB implementation of the Summary Repository."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from bson.binary import Binary, UuidRepresentation
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import ASCENDING, DESCENDING

from app.application.interfaces.summary_repository import Summary, SummaryRepository


def _to_document(summary: Summary) -> dict:
    return {
        "_id": Binary.from_uuid(summary.id, UuidRepresentation.STANDARD),
        "original_filename": summary.original_filename,
        "summary_text": summary.summary_text,
        "extracted_text": summary.extracted_text,
        "created_at": summary.created_at,
    }


def _from_document(doc: dict) -> Summary:
    doc_id = doc["_id"]
    if isinstance(doc_id, Binary):
        summary_id = doc_id.as_uuid()
    else:
        summary_id = doc_id
    return Summary(
        id=summary_id,
        original_filename=doc["original_filename"],
        summary_text=doc["summary_text"],
        extracted_text=doc["extracted_text"],
        created_at=doc["created_at"],
    )


class MongoSummaryRepository(SummaryRepository):
    def __init__(self, client: AsyncIOMotorClient, db_name: str = "appdb"):
        self._client = client
        self._collection: AsyncIOMotorCollection = client[db_name]["summaries"]

    @classmethod
    async def from_uri(cls, uri: str, db_name: str = "appdb") -> "MongoSummaryRepository":
        client = AsyncIOMotorClient(uri, uuidRepresentation="standard")
        await client.admin.command("ping")
        repo = cls(client, db_name)
        await repo._create_indexes()
        return repo

    async def _create_indexes(self) -> None:
        await self._collection.create_index([("created_at", DESCENDING)])
        await self._collection.create_index([("original_filename", ASCENDING)])

    async def save(self, summary: Summary) -> Summary:
        if summary.id is None:
            summary.id = uuid4()
        if summary.created_at is None:
            summary.created_at = datetime.now(timezone.utc)

        document = _to_document(summary)
        await self._collection.replace_one(
            {"_id": document["_id"]}, document, upsert=True
        )
        return summary

    async def get_by_id(self, summary_id: UUID) -> Summary | None:
        doc = await self._collection.find_one({
            "_id": Binary.from_uuid(summary_id, UuidRepresentation.STANDARD)
        })
        return _from_document(doc) if doc else None

    async def get_all(self, limit: int = 100) -> list[Summary]:
        cursor = self._collection.find().sort("created_at", DESCENDING).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [_from_document(doc) for doc in docs]

    async def close(self) -> None:
        self._client.close()
