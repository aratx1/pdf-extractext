"""Tests de los endpoints HTTP.

El servicio se sustituye por uno con dobles de prueba, así que no hay red ni BD.
"""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.application.services.pdf_service import PDFService
from app.application.services.summary_service import SummaryService
from app.main import app
from app.presentation.routers import pdf_summary as router_module

DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


@pytest.fixture
def service(fake_ai_provider, fake_repository) -> SummaryService:
    return SummaryService(
        pdf_service=PDFService(),
        ai_provider=fake_ai_provider,
        repository=fake_repository,
    )


@pytest.fixture
def client(service) -> TestClient:
    app.dependency_overrides[router_module.get_summary_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def subir_pdf(client, pdf_bytes, filename="documento.pdf"):
    return client.post(
        "/api/summarize",
        files={"file": (filename, pdf_bytes, "application/pdf")},
    )


# --- POST /api/summarize ---


def test_summarize_devuelve_200_con_un_pdf_valido(client, pdf_bytes):
    assert subir_pdf(client, pdf_bytes).status_code == 200


def test_summarize_devuelve_el_resumen_y_el_nombre_original(client, pdf_bytes):
    body = subir_pdf(client, pdf_bytes).json()

    assert body["summary_text"] == "Resumen de prueba"
    assert body["original_filename"] == "documento.pdf"


def test_summarize_devuelve_un_id_y_una_fecha(client, pdf_bytes):
    body = subir_pdf(client, pdf_bytes).json()

    assert body["id"]
    assert body["created_at"]


def test_summarize_rechaza_un_archivo_que_no_es_pdf(client, pdf_bytes):
    response = subir_pdf(client, pdf_bytes, filename="documento.txt")

    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_summarize_rechaza_un_archivo_vacio(client):
    response = client.post(
        "/api/summarize",
        files={"file": ("vacio.pdf", b"", "application/pdf")},
    )

    assert response.status_code == 400


def test_summarize_sin_archivo_devuelve_422(client):
    assert client.post("/api/summarize").status_code == 422


# --- GET /api/summaries ---


def test_lista_vacia_al_principio(client):
    body = client.get("/api/summaries").json()

    assert body["summaries"] == []
    assert body["total"] == 0


def test_lista_los_resumenes_creados(client, pdf_bytes):
    subir_pdf(client, pdf_bytes, "uno.pdf")
    subir_pdf(client, pdf_bytes, "dos.pdf")

    body = client.get("/api/summaries").json()

    assert body["total"] == 2


def test_lista_respeta_el_parametro_limit(client, pdf_bytes):
    subir_pdf(client, pdf_bytes, "uno.pdf")
    subir_pdf(client, pdf_bytes, "dos.pdf")

    body = client.get("/api/summaries?limit=1").json()

    assert body["total"] == 1


# --- GET /api/summaries/{id} ---


def test_devuelve_un_resumen_por_su_id(client, pdf_bytes):
    creado = subir_pdf(client, pdf_bytes).json()

    response = client.get(f"/api/summaries/{creado['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == creado["id"]


def test_devuelve_404_si_el_id_no_existe(client):
    assert client.get(f"/api/summaries/{uuid4()}").status_code == 404


def test_devuelve_422_si_el_id_no_es_un_uuid(client):
    assert client.get("/api/summaries/no-es-un-uuid").status_code == 422


# --- GET /api/summaries/{id}/export ---


def test_export_devuelve_un_docx(client, pdf_bytes):
    creado = subir_pdf(client, pdf_bytes).json()

    response = client.get(f"/api/summaries/{creado['id']}/export")

    assert response.status_code == 200
    assert response.headers["content-type"] == DOCX_MIME


def test_export_propone_un_nombre_de_archivo(client, pdf_bytes):
    creado = subir_pdf(client, pdf_bytes).json()

    response = client.get(f"/api/summaries/{creado['id']}/export")

    assert "attachment" in response.headers["content-disposition"]
    assert "resumen_documento.docx" in response.headers["content-disposition"]


def test_export_devuelve_un_archivo_no_vacio(client, pdf_bytes):
    creado = subir_pdf(client, pdf_bytes).json()

    response = client.get(f"/api/summaries/{creado['id']}/export")

    assert response.content.startswith(b"PK")  # un .docx es un zip


def test_export_devuelve_404_si_el_id_no_existe(client):
    assert client.get(f"/api/summaries/{uuid4()}/export").status_code == 404


# --- GET /api/health ---


def test_health_responde_healthy_si_la_ia_esta_disponible(client):
    body = client.get("/api/health").json()

    assert body["status"] == "healthy"
    assert body["ai_provider_available"] is True


def test_health_responde_degraded_si_la_ia_no_esta_disponible(
    client, fake_ai_provider
):
    fake_ai_provider.healthy = False

    body = client.get("/api/health").json()

    assert body["status"] == "degraded"
    assert body["ai_provider_available"] is False
