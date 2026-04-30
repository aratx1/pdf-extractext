"""
app/pdf_service.py
------------------
Servicio principal de extracción de texto de PDFs.

Detecta automáticamente si un PDF tiene texto real o es un PDF escaneado
(imagen), y usa la técnica correcta en cada caso:

  - PDF con texto real → pdfplumber (rápido y preciso)
  - PDF escaneado/imagen → OCR con pytesseract (más lento pero necesario)

Este módulo es el punto de entrada principal para procesar PDFs. (Issue #17)
"""

import pdfplumber

from app.ocr import extract_text_with_ocr
from app.pdf_extractor import extract_text_from_pdf

# Mínimo de caracteres por página para considerar que el PDF tiene texto real.
# Si una página tiene menos que esto, se asume que es una imagen escaneada.
MIN_CHARS_PER_PAGE = 20


def is_scanned_pdf(pdf_path: str) -> bool:
    """
    Detecta si un PDF es escaneado (imagen) o tiene texto real.

    Abre el PDF con pdfplumber e intenta extraer texto de las primeras páginas.
    Si el promedio de caracteres por página es muy bajo, se considera escaneado.

    Args:
        pdf_path: Ruta al archivo PDF.

    Returns:
        True si el PDF parece escaneado, False si tiene texto real.
    """
    with pdfplumber.open(pdf_path) as pdf:
        if not pdf.pages:
            return False

        # Revisamos hasta las primeras 3 páginas para decidir
        pages_to_check = pdf.pages[:3]
        total_chars = 0

        for page in pages_to_check:
            text = page.extract_text() or ""
            total_chars += len(text.strip())

        average_chars = total_chars / len(pages_to_check)
        return average_chars < MIN_CHARS_PER_PAGE


def process_pdf(pdf_path: str, ocr_language: str = "spa") -> dict:
    """
    Procesa un PDF y devuelve su texto usando el método adecuado.

    Detecta automáticamente si el PDF tiene texto real o es escaneado,
    y aplica pdfplumber u OCR según corresponda.

    Args:
        pdf_path: Ruta al archivo PDF.
        ocr_language: Idioma para el OCR si se necesita (default: "spa").

    Returns:
        Diccionario con:
          - "text": el texto extraído
          - "method": "pdfplumber" u "ocr" según qué se usó
          - "scanned": True/False

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archivo no es un PDF.
        RuntimeError: Si el OCR falla por falta de Tesseract/Poppler.
    """
    scanned = is_scanned_pdf(pdf_path)

    if scanned:
        text = extract_text_with_ocr(pdf_path, language=ocr_language)
        method = "ocr"
    else:
        text = extract_text_from_pdf(pdf_path)
        method = "pdfplumber"

    return {
        "text": text,
        "method": method,
        "scanned": scanned,
    }
