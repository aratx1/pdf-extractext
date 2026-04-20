"""
tests/test_pdf_extractor.py
---------------------------
Tests para app/pdf_extractor.py usando unittest + pytest.

"""

import os
import sys
import unittest
import tempfile

# Permite importar desde la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pdf_extractor import extract_text_from_pdf


class TestExtractTextFromPdf(unittest.TestCase):

    # --- Casos de error esperado ---

    def test_archivo_no_existe_lanza_error(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        with self.assertRaises(FileNotFoundError):
            extract_text_from_pdf("no_existe.pdf")

    def test_extension_incorrecta_lanza_error(self):
        """Debe lanzar ValueError si el archivo no es .pdf."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"texto de prueba")
            tmp_path = tmp.name
        try:
            with self.assertRaises(ValueError):
                extract_text_from_pdf(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_ruta_vacia_lanza_error(self):
        """Debe lanzar FileNotFoundError si se pasa una ruta vacía."""
        with self.assertRaises(FileNotFoundError):
            extract_text_from_pdf("")

    # --- Casos con PDF real (se activan cuando exista tests/sample.pdf) ---

    def test_retorna_string(self):
        pdf_prueba = os.path.join(os.path.dirname(__file__), "sample.pdf")
        if not os.path.exists(pdf_prueba):
            self.skipTest("Agregá un PDF en tests/sample.pdf para activar este test.")
        resultado = extract_text_from_pdf(pdf_prueba)
        self.assertIsInstance(resultado, str)

    def test_texto_no_esta_vacio(self):
        pdf_prueba = os.path.join(os.path.dirname(__file__), "sample.pdf")
        if not os.path.exists(pdf_prueba):
            self.skipTest("Agregá un PDF en tests/sample.pdf para activar este test.")
        resultado = extract_text_from_pdf(pdf_prueba)
        self.assertGreater(len(resultado), 0)

    def test_texto_contiene_separador_paginas(self):
        pdf_prueba = os.path.join(os.path.dirname(__file__), "sample.pdf")
        if not os.path.exists(pdf_prueba):
            self.skipTest("Agregá un PDF en tests/sample.pdf para activar este test.")
        resultado = extract_text_from_pdf(pdf_prueba)
        self.assertIn("--- Página", resultado)


if __name__ == "__main__":
    unittest.main()
