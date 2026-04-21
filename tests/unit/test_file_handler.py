from pathlib import Path

import pytest

from app.infrastructure.file_storage.file_handler import FileHandler


class FakeAsyncFile:
    def __init__(self, storage: dict[Path, bytes], file_path: Path, mode: str):
        self._storage = storage
        self._file_path = file_path
        self._mode = mode

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def write(self, content: bytes):
        if "w" not in self._mode:
            raise AssertionError("write called with non-write mode")
        self._storage[self._file_path] = content

    async def read(self):
        if "r" not in self._mode:
            raise AssertionError("read called with non-read mode")
        return self._storage[self._file_path]


@pytest.mark.asyncio
async def test_file_handler_save_read_exists_and_delete(monkeypatch):
    storage: dict[Path, bytes] = {}
    upload_dir = Path("virtual-uploads")

    def fake_open(file_path: Path, mode: str):
        return FakeAsyncFile(storage, Path(file_path), mode)

    def fake_exists(path: Path):
        return Path(path) in storage

    def fake_unlink(path: Path):
        storage.pop(Path(path), None)

    monkeypatch.setattr(
        "app.infrastructure.file_storage.file_handler.aiofiles.open",
        fake_open,
    )
    monkeypatch.setattr(Path, "exists", fake_exists)
    monkeypatch.setattr(Path, "unlink", fake_unlink)

    handler = FileHandler(upload_dir=upload_dir)
    content = b"pdf bytes"
    filename = "document.pdf"

    saved_path = await handler.save(content, filename)

    assert saved_path == upload_dir / filename
    assert handler.exists(filename) is True
    assert await handler.read(filename) == content

    handler.delete(filename)

    assert handler.exists(filename) is False
