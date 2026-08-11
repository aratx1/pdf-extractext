"""Tests de integración del repositorio de MongoDB.

Necesitan un MongoDB en marcha (`docker compose up -d mongodb`). Se saltan
solos si no hay conexión. Para ejecutarlos:

    pytest -m integration

Usan una base de datos aparte (`pdf_extractext_test`) que se limpia al terminar,
para no tocar los datos reales.
"""

from datetime import datetime
from uuid import UUID, uuid4

import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from app.application.interfaces.summary_repository import Summary
from app.core import get_settings
from app.infrastructure.repositories.mongo_repository import MongoSummaryRepository

pytestmark = pytest.mark.integration

TEST_DB = "pdf_extractext_test"


@pytest.fixture
async def repo():
    url = get_settings().mongodb_url
    client = AsyncIOMotorClient(url, serverSelectionTimeoutMS=1500)
    try:
        await client.admin.command("ping")
    except PyMongoError:
        client.close()
        pytest.skip(f"no hay un MongoDB accesible en {url}")

    await client.drop_database(TEST_DB)
    yield MongoSummaryRepository(mongodb_url=url, db_name=TEST_DB)
    await client.drop_database(TEST_DB)
    client.close()


def make_summary(filename: str = "documento.pdf") -> Summary:
    return Summary(
        id=None,
        original_filename=filename,
        summary_text="Un resumen",
        extracted_text="Texto extraido",
        created_at=None,
    )


async def test_save_asigna_id_y_fecha(repo):
    saved = await repo.save(make_summary())

    assert isinstance(saved.id, UUID)
    assert isinstance(saved.created_at, datetime)


async def test_lo_guardado_se_recupera_por_id(repo):
    saved = await repo.save(make_summary("informe.pdf"))

    found = await repo.get_by_id(saved.id)

    assert found is not None
    assert found.id == saved.id
    assert found.original_filename == "informe.pdf"
    assert found.summary_text == "Un resumen"
    assert found.extracted_text == "Texto extraido"


async def test_get_by_id_devuelve_none_si_no_existe(repo):
    assert await repo.get_by_id(uuid4()) is None


async def test_get_all_devuelve_los_guardados(repo):
    await repo.save(make_summary("uno.pdf"))
    await repo.save(make_summary("dos.pdf"))

    assert len(await repo.get_all()) == 2


async def test_get_all_ordena_del_mas_reciente_al_mas_antiguo(repo):
    await repo.save(make_summary("antiguo.pdf"))
    await repo.save(make_summary("reciente.pdf"))

    result = await repo.get_all()

    assert [s.original_filename for s in result] == ["reciente.pdf", "antiguo.pdf"]


async def test_get_all_respeta_el_limite(repo):
    await repo.save(make_summary("uno.pdf"))
    await repo.save(make_summary("dos.pdf"))

    assert len(await repo.get_all(limit=1)) == 1


async def test_get_all_devuelve_lista_vacia_si_no_hay_nada(repo):
    assert await repo.get_all() == []
