"""
tests/test_pdf_service.py
--------------------------
Tests para app/pdf_service.py y app/ocr.py usando unittest + pytest. (Issue #17)

Nota: los tests que requieren un PDF real o Tesseract instalado se saltean
automáticamente si no están disponibles en el entorno.

Para correr: pytest tests/test_pdf_service.py -v
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pdf_service import is_scanned_pdf, process_pdf, MIN_CHARS_PER_PAGE


class TestIsScanedPdf(unittest.TestCase):
    """Tests para la detección automática de PDFs escaneados."""

    def test_pdf_con_texto_no_es_escaneado(self):
        """Un PDF con bastante texto debe devolver False."""
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "A" * 200  # texto largo

        with patch("app.pdf_service.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value.pages = [mock_page]
            resultado = is_scanned_pdf("fake.pdf")

        self.assertFalse(resultado)

    def test_pdf_sin_texto_es_escaneado(self):
        """Un PDF sin texto (escaneado) debe devolver True."""
        mock_page = MagicMock()
        mock_page.extract_text.return_value = ""  # sin texto

        with patch("app.pdf_service.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value.pages = [mock_page]
            resultado = is_scanned_pdf("fake.pdf")

        self.assertTrue(resultado)

    def test_pdf_con_poco_texto_es_escaneado(self):
        """Un PDF con menos caracteres que el mínimo debe considerarse escaneado."""
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "abc"  # menos de MIN_CHARS_PER_PAGE

        with patch("app.pdf_service.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value.pages = [mock_page]
            resultado = is_scanned_pdf("fake.pdf")

        self.assertTrue(resultado)

    def test_constante_minimo_tiene_valor_razonable(self):
        """El umbral mínimo de caracteres debe ser positivo y razonable."""
        self.assertGreater(MIN_CHARS_PER_PAGE, 0)
        self.assertLess(MIN_CHARS_PER_PAGE, 100)


class TestProcessPdf(unittest.TestCase):
    """Tests para el servicio principal de procesamiento."""

    def test_pdf_normal_usa_pdfplumber(self):
        """Un PDF con texto debe procesarse con pdfplumber."""
        with patch("app.pdf_service.is_scanned_pdf", return_value=False), \
             patch("app.pdf_service.extract_text_from_pdf", return_value="texto extraído"):

            resultado = process_pdf("fake.pdf")

        self.assertEqual(resultado["method"], "pdfplumber")
        self.assertFalse(resultado["scanned"])
        self.assertEqual(resultado["text"], "texto extraído")

    def test_pdf_escaneado_usa_ocr(self):
        """Un PDF escaneado debe procesarse con OCR."""
        with patch("app.pdf_service.is_scanned_pdf", return_value=True), \
             patch("app.pdf_service.extract_text_with_ocr", return_value="texto ocr"):

            resultado = process_pdf("fake.pdf")

        self.assertEqual(resultado["method"], "ocr")
        self.assertTrue(resultado["scanned"])
        self.assertEqual(resultado["text"], "texto ocr")

    def test_resultado_tiene_claves_correctas(self):
        """El resultado siempre debe tener las claves text, method y scanned."""
        with patch("app.pdf_service.is_scanned_pdf", return_value=False), \
             patch("app.pdf_service.extract_text_from_pdf", return_value="texto"):

            resultado = process_pdf("fake.pdf")

        self.assertIn("text", resultado)
        self.assertIn("method", resultado)
        self.assertIn("scanned", resultado)

    def test_pdf_real_con_texto(self):
        """Test con PDF real si existe tests/sample.pdf."""
        pdf_prueba = os.path.join(os.path.dirname(__file__), "sample.pdf")
        if not os.path.exists(pdf_prueba):
            self.skipTest("Agregá un PDF en tests/sample.pdf para activar este test.")

        resultado = process_pdf(pdf_prueba)
        self.assertIsInstance(resultado["text"], str)
        self.assertIn(resultado["method"], ["pdfplumber", "ocr"])
        self.assertIsInstance(resultado["scanned"], bool)


if __name__ == "__main__":
    unittest.main()
