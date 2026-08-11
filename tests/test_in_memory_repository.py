"""Tests del repositorio en memoria."""

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest

from app.application.interfaces.summary_repository import Summary
from app.infrastructure.repositories.in_memory_repository import InMemorySummaryRepository


@pytest.fixture
def repo() -> InMemorySummaryRepository:
    return InMemorySummaryRepository()


def make_summary(filename: str = "documento.pdf") -> Summary:
    return Summary(
        id=None,
        original_filename=filename,
        summary_text="Un resumen",
        extracted_text="Texto extraido",
        created_at=None,
    )


async def test_save_asigna_un_uuid(repo):
    saved = await repo.save(make_summary())

    assert isinstance(saved.id, UUID)


async def test_save_asigna_la_fecha_de_creacion(repo):
    saved = await repo.save(make_summary())

    assert isinstance(saved.created_at, datetime)


async def test_save_asigna_ids_distintos(repo):
    primero = await repo.save(make_summary("uno.pdf"))
    segundo = await repo.save(make_summary("dos.pdf"))

    assert primero.id != segundo.id


async def test_get_by_id_devuelve_el_resumen_guardado(repo):
    saved = await repo.save(make_summary())

    assert await repo.get_by_id(saved.id) is saved


async def test_get_by_id_devuelve_none_si_no_existe(repo):
    assert await repo.get_by_id(uuid4()) is None


async def test_get_all_devuelve_todos_los_guardados(repo):
    await repo.save(make_summary("uno.pdf"))
    await repo.save(make_summary("dos.pdf"))

    assert len(await repo.get_all()) == 2


async def test_get_all_ordena_del_mas_reciente_al_mas_antiguo(repo):
    antiguo = await repo.save(make_summary("antiguo.pdf"))
    reciente = await repo.save(make_summary("reciente.pdf"))
    antiguo.created_at = datetime.now(timezone.utc) - timedelta(days=1)

    result = await repo.get_all()

    assert [s.original_filename for s in result] == ["reciente.pdf", "antiguo.pdf"]


async def test_get_all_respeta_el_limite(repo):
    await repo.save(make_summary("uno.pdf"))
    await repo.save(make_summary("dos.pdf"))

    assert len(await repo.get_all(limit=1)) == 1


async def test_get_all_devuelve_lista_vacia_si_no_hay_nada(repo):
    assert await repo.get_all() == []
