"""
tests/test_text_structure.py
-----------------------------
Tests para app/text_structure.py usando unittest + pytest. (Issue #16)

Para correr: pytest tests/test_text_structure.py -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.text_structure import detect_structure


class TestDetectStructure(unittest.TestCase):

    # --- Texto vacío ---

    def test_texto_vacio_devuelve_vacio(self):
        self.assertEqual(detect_structure(""), "")

    def test_texto_solo_espacios_devuelve_igual(self):
        resultado = detect_structure("   ")
        self.assertEqual(resultado.strip(), "")

    # --- Títulos ---

    def test_detecta_titulo_en_mayusculas(self):
        texto = "INTRODUCCIÓN\nEste es el cuerpo del texto."
        resultado = detect_structure(texto)
        self.assertIn("## Introducción", resultado)

    def test_detecta_subtitulo_linea_corta_sin_punto(self):
        texto = "\nMetodología\nEste es el cuerpo del texto con más detalle."
        resultado = detect_structure(texto)
        self.assertIn("### Metodología", resultado)

    def test_linea_larga_no_es_titulo(self):
        texto = "Esta es una línea muy larga que supera los ochenta caracteres y definitivamente no es un título.\nOtro párrafo."
        resultado = detect_structure(texto)
        self.assertNotIn("##", resultado)

    # --- Viñetas y listas ---

    def test_detecta_vineta_guion(self):
        resultado = detect_structure("- Primer ítem")
        self.assertIn("- Primer ítem", resultado)

    def test_detecta_vineta_punto(self):
        resultado = detect_structure("• Segundo ítem")
        self.assertIn("- Segundo ítem", resultado)

    def test_detecta_lista_numerada(self):
        resultado = detect_structure("1. Primer paso")
        self.assertIn("1. Primer paso", resultado)

    def test_detecta_lista_con_parentesis(self):
        resultado = detect_structure("1) Primer ítem")
        self.assertIn("1) Primer ítem", resultado)

    # --- Párrafos ---

    def test_preserva_separacion_entre_parrafos(self):
        texto = "Primer párrafo con contenido.\n\nSegundo párrafo con más contenido."
        resultado = detect_structure(texto)
        self.assertIn("\n\n", resultado)

    # --- Caso completo ---

    def test_estructura_completa(self):
        texto = (
            "RESUMEN EJECUTIVO\n"
            "Este documento presenta los hallazgos del estudio.\n"
            "\n"
            "Objetivos\n"
            "Se plantearon los siguientes objetivos principales.\n"
            "\n"
            "- Analizar los datos disponibles\n"
            "- Identificar patrones relevantes\n"
            "1. Primer paso del proceso\n"
        )
        resultado = detect_structure(texto)
        self.assertIn("## Resumen Ejecutivo", resultado)
        self.assertIn("### Objetivos", resultado)
        self.assertIn("- Analizar los datos disponibles", resultado)
        self.assertIn("1. Primer paso del proceso", resultado)


if __name__ == "__main__":
    unittest.main()
