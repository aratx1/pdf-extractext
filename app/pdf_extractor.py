"""
app/pdf_extractor.py
--------------------
Script básico para leer un archivo PDF y devolver su texto.

## Investigación de librerías (Issue #6)

| Librería   | Pros                                          | Contras                                      | Veredicto     |
|------------|-----------------------------------------------|----------------------------------------------|---------------|
| PyPDF2     | Muy conocida, mucha documentación             | DEPRECADA, reemplazada por pypdf             | ❌ No usar    |
| pymupdf    | Muy rápida, extrae texto con mucha precisión  | Requiere binarios del sistema, más compleja  | ⚠️  Opcional  |
| pdfplumber | Simple, excelente extracción de texto/tablas  | Más lenta que pymupdf en PDFs grandes        | ✅ ELEGIDA    |

Decisión: pdfplumber es la mejor opción para empezar. Es simple, bien mantenida
y produce resultados de calidad. pymupdf puede considerarse si se necesita
mayor performance en el futuro.
"""

import os
import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Lee un archivo PDF y devuelve todo su texto como string.

    Args:
        pdf_path: Ruta al archivo PDF.

    Returns:
        Texto extraído del PDF, con separadores por página.

    Raises:
        FileNotFoundError: Si el archivo no existe en esa ruta.
        ValueError: Si el archivo no tiene extensión .pdf.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo no existe: {pdf_path}")

    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError(f"El archivo no es un PDF: {pdf_path}")

    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                full_text += f"--- Página {i + 1} ---\n"
                full_text += page_text + "\n\n"

    return full_text
