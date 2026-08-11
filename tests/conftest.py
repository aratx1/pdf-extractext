"""Fixtures compartidas por la suite de tests."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from app.application.interfaces.ai_provider import AIProvider, AIResponse
from app.application.interfaces.summary_repository import Summary, SummaryRepository


def build_pdf(pages: list[str]) -> bytes:
    """Construye un PDF mínimo y válido con el texto indicado, una página por elemento.

    Se genera a mano para no añadir una dependencia (reportlab) que solo harían
    falta en los tests. El resultado es legible por pypdf.
    """
    objects: list[bytes] = []

    # 1: catálogo, 2: árbol de páginas, 3: fuente
    page_ids = [4 + i for i in range(len(pages))]
    content_ids = [4 + len(pages) + i for i in range(len(pages))]

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = b" ".join(b"%d 0 R" % pid for pid in page_ids)
    objects.append(
        b"<< /Type /Pages /Kids [" + kids + b"] /Count %d >>" % len(pages)
    )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    for page_id, content_id in zip(page_ids, content_ids):
        objects.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 3 0 R >> >> "
            b"/Contents %d 0 R >>" % content_id
        )

    for text in pages:
        escaped = text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
        stream = (
            b"BT /F1 12 Tf 72 720 Td (" + escaped.encode("latin-1") + b") Tj ET"
        )
        objects.append(
            b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"
        )

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"

    xref_offset = len(out)
    out += b"xref\n0 %d\n" % (len(objects) + 1)
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\n" % (len(objects) + 1)
    out += b"startxref\n%d\n%%%%EOF\n" % xref_offset

    return bytes(out)


@pytest.fixture
def pdf_bytes() -> bytes:
    """PDF de una página con texto conocido."""
    return build_pdf(["Hola mundo desde un PDF de prueba"])


@pytest.fixture
def multipage_pdf_bytes() -> bytes:
    """PDF de dos páginas con texto distinto en cada una."""
    return build_pdf(["Primera pagina", "Segunda pagina"])


class FakeAIProvider(AIProvider):
    """Proveedor de IA de mentira: registra lo que recibe y devuelve algo fijo."""

    def __init__(self, content: str = "Resumen de prueba", healthy: bool = True):
        self.content = content
        self.healthy = healthy
        self.received_text: str | None = None
        self.received_max_length: int | None = None
        self.calls = 0

    async def generate_summary(self, text: str, max_length: int = 500) -> AIResponse:
        self.calls += 1
        self.received_text = text
        self.received_max_length = max_length
        return AIResponse(content=self.content, model="fake-model", tokens_used=42)

    async def health_check(self) -> bool:
        return self.healthy


class FakeRepository(SummaryRepository):
    """Repositorio de mentira, en memoria, para aislar los tests del servicio."""

    def __init__(self):
        self.saved: list[Summary] = []
        self._storage: dict[UUID, Summary] = {}

    async def save(self, summary: Summary) -> Summary:
        summary.id = summary.id or uuid4()
        summary.created_at = summary.created_at or datetime.now(timezone.utc)
        self.saved.append(summary)
        self._storage[summary.id] = summary
        return summary

    async def get_by_id(self, summary_id: UUID) -> Summary | None:
        return self._storage.get(summary_id)

    async def get_all(self, limit: int = 100) -> list[Summary]:
        return list(self._storage.values())[:limit]


@pytest.fixture
def fake_ai_provider() -> FakeAIProvider:
    return FakeAIProvider()


@pytest.fixture
def fake_repository() -> FakeRepository:
    return FakeRepository()
