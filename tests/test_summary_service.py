"""Tests de la orquestación: PDF -> IA -> persistencia.

Usan dobles de prueba, así que no tocan red ni base de datos.
"""

from uuid import uuid4

import pytest

from app.application.services.pdf_service import PDFService
from app.application.services.summary_service import MAX_PROMPT_CHARS, SummaryService
from tests.conftest import build_pdf


@pytest.fixture
def service(fake_ai_provider, fake_repository) -> SummaryService:
    return SummaryService(
        pdf_service=PDFService(),
        ai_provider=fake_ai_provider,
        repository=fake_repository,
    )


async def test_devuelve_el_resumen_generado_por_la_ia(service, fake_ai_provider, pdf_bytes):
    fake_ai_provider.content = "Este es el resumen"

    summary = await service.create_summary(pdf_bytes, "documento.pdf")

    assert summary.summary_text == "Este es el resumen"


async def test_guarda_el_resumen_en_el_repositorio(service, fake_repository, pdf_bytes):
    await service.create_summary(pdf_bytes, "documento.pdf")

    assert len(fake_repository.saved) == 1
    assert fake_repository.saved[0].original_filename == "documento.pdf"


async def test_envia_a_la_ia_el_texto_extraido(service, fake_ai_provider, pdf_bytes):
    await service.create_summary(pdf_bytes, "documento.pdf")

    assert fake_ai_provider.received_text == "Hola mundo desde un PDF de prueba"


async def test_trunca_el_texto_enviado_a_la_ia(service, fake_ai_provider):
    pdf = build_pdf(["A" * (MAX_PROMPT_CHARS + 5000)])

    await service.create_summary(pdf, "largo.pdf")

    assert len(fake_ai_provider.received_text) == MAX_PROMPT_CHARS


async def test_guarda_solo_los_primeros_1000_caracteres_extraidos(service, fake_repository):
    pdf = build_pdf(["B" * 3000])

    summary = await service.create_summary(pdf, "largo.pdf")

    assert len(summary.extracted_text) == 1000


async def test_llama_una_sola_vez_a_la_ia(service, fake_ai_provider, pdf_bytes):
    await service.create_summary(pdf_bytes, "documento.pdf")

    assert fake_ai_provider.calls == 1


async def test_get_summary_devuelve_lo_guardado(service, pdf_bytes):
    created = await service.create_summary(pdf_bytes, "documento.pdf")

    found = await service.get_summary(created.id)

    assert found is created


async def test_get_summary_devuelve_none_si_no_existe(service):
    assert await service.get_summary(uuid4()) is None


async def test_list_summaries_devuelve_todos(service, pdf_bytes):
    await service.create_summary(pdf_bytes, "uno.pdf")
    await service.create_summary(pdf_bytes, "dos.pdf")

    assert len(await service.list_summaries()) == 2


async def test_list_summaries_respeta_el_limite(service, pdf_bytes):
    await service.create_summary(pdf_bytes, "uno.pdf")
    await service.create_summary(pdf_bytes, "dos.pdf")

    assert len(await service.list_summaries(limit=1)) == 1
