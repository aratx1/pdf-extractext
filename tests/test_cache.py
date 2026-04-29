"""
tests/test_cache.py
-------------------
Tests para app/cache.py usando unittest + pytest. (Issue #11)

Para correr: pytest tests/test_cache.py -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.cache import get_cached_summary, save_summary_to_cache, CACHE_FILE


class TestCache(unittest.TestCase):

    def setUp(self):
        """Elimina el archivo de caché antes de cada test para empezar limpio."""
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)

    def tearDown(self):
        """Elimina el archivo de caché después de cada test."""
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)

    # --- Tests principales ---

    def test_cache_vacio_devuelve_none(self):
        """Si no hay caché, debe devolver None."""
        resultado = get_cached_summary("texto de prueba")
        self.assertIsNone(resultado)

    def test_guardar_y_recuperar_resumen(self):
        """Después de guardar un resumen, debe poder recuperarse."""
        texto = "Este es el contenido del PDF."
        resumen = "Este es el resumen generado."

        save_summary_to_cache(texto, resumen)
        resultado = get_cached_summary(texto)

        self.assertEqual(resultado, resumen)

    def test_texto_diferente_no_encuentra_cache(self):
        """Un texto distinto no debe encontrar el caché de otro texto."""
        save_summary_to_cache("texto A", "resumen A")
        resultado = get_cached_summary("texto B")
        self.assertIsNone(resultado)

    def test_mismo_contenido_mismo_hash(self):
        """Dos textos idénticos deben encontrar el mismo caché."""
        texto = "Contenido idéntico."
        resumen = "Resumen del contenido."

        save_summary_to_cache(texto, resumen)

        # Simula un segundo PDF con el mismo contenido
        resultado = get_cached_summary(texto)
        self.assertEqual(resultado, resumen)

    def test_sobreescribir_resumen(self):
        """Guardar un nuevo resumen para el mismo texto debe actualizarlo."""
        texto = "Texto de prueba."
        save_summary_to_cache(texto, "resumen viejo")
        save_summary_to_cache(texto, "resumen nuevo")
        resultado = get_cached_summary(texto)
        self.assertEqual(resultado, "resumen nuevo")

    def test_cache_persiste_en_archivo(self):
        """El caché debe guardarse en un archivo JSON."""
        save_summary_to_cache("texto", "resumen")
        self.assertTrue(os.path.exists(CACHE_FILE))


if __name__ == "__main__":
    unittest.main()
