"""Tests de la extracción de texto de PDFs."""

import pytest

from app.application.services.pdf_service import PDFService
from tests.conftest import build_pdf


@pytest.fixture
def service() -> PDFService:
    return PDFService()


def test_extrae_el_texto_de_un_pdf_de_una_pagina(service, pdf_bytes):
    result = service.extract_text(pdf_bytes, "documento.pdf")

    assert result.text == "Hola mundo desde un PDF de prueba"


def test_conserva_el_nombre_del_archivo(service, pdf_bytes):
    result = service.extract_text(pdf_bytes, "documento.pdf")

    assert result.filename == "documento.pdf"


def test_cuenta_las_paginas(service, multipage_pdf_bytes):
    result = service.extract_text(multipage_pdf_bytes, "documento.pdf")

    assert result.page_count == 2


def test_une_las_paginas_con_doble_salto_de_linea(service, multipage_pdf_bytes):
    result = service.extract_text(multipage_pdf_bytes, "documento.pdf")

    assert result.text == "Primera pagina\n\nSegunda pagina"


def test_character_count_coincide_con_el_texto_extraido(service, multipage_pdf_bytes):
    result = service.extract_text(multipage_pdf_bytes, "documento.pdf")

    assert result.character_count == len(result.text)


def test_una_pagina_sin_texto_no_rompe_la_extraccion(service):
    pdf = build_pdf(["", "Con texto"])

    result = service.extract_text(pdf, "documento.pdf")

    assert result.text == "Con texto"
    assert result.page_count == 2


def test_un_pdf_sin_texto_devuelve_cadena_vacia(service):
    pdf = build_pdf([""])

    result = service.extract_text(pdf, "documento.pdf")

    assert result.text == ""
    assert result.character_count == 0


def test_bytes_que_no_son_un_pdf_lanzan_error(service):
    with pytest.raises(Exception):
        service.extract_text(b"esto no es un pdf", "falso.pdf")
