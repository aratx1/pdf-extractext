"""Pytest configuration and shared fixtures."""

import pytest
from datetime import datetime, timezone
from uuid import uuid4

import docker
from motor.motor_asyncio import AsyncIOMotorClient
from testcontainers.mongodb import MongoDbContainer

from app.application.interfaces.summary_repository import Summary
from app.infrastructure.repositories.in_memory_repository import (
    InMemorySummaryRepository,
)
from app.infrastructure.repositories.mongo_repository import MongoSummaryRepository


def pytest_addoption(parser):
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests requiring Docker",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires Docker)"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-integration"):
        return
    skip_integration = pytest.mark.skip(
        reason="need --run-integration option to run Docker-based tests"
    )
    for item in items:
        if item.get_closest_marker("integration"):
            item.add_marker(skip_integration)


def _docker_available() -> bool:
    try:
        client = docker.from_env()
        client.ping()
        return True
    except Exception:
        return False


@pytest.fixture
def in_memory_repository():
    return InMemorySummaryRepository()


@pytest.fixture
def sample_summary():
    return Summary(
        id=None,
        original_filename="test.pdf",
        summary_text="This is a summary of the document.",
        extracted_text="Extracted text preview from the PDF...",
        created_at=None,
    )


@pytest.fixture(scope="session")
def mongodb_container():
    if not _docker_available():
        pytest.skip("Docker not available")
    with MongoDbContainer("mongo:7.0") as container:
        yield container


@pytest.fixture
def mongo_uri(mongodb_container: MongoDbContainer):
    return mongodb_container.get_connection_url()


@pytest.fixture
async def mongo_repository(mongo_uri: str):
    repo = await MongoSummaryRepository.from_uri(mongo_uri, db_name="testdb")
    yield repo
    await repo._collection.drop()
    await repo.close()


@pytest.fixture
async def mongo_client(mongo_uri: str):
    client = AsyncIOMotorClient(mongo_uri)
    yield client
    client.close()
