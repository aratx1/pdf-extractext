"""
app/ocr.py
----------
Módulo de OCR (Reconocimiento Óptico de Caracteres) para PDFs escaneados.

Los PDFs escaneados son imágenes — no tienen texto real adentro, solo píxeles.
pdfplumber no puede extraer texto de ellos. Este módulo convierte cada página
del PDF en una imagen y luego le aplica OCR con pytesseract para leer el texto.

Dependencias del sistema requeridas:
  - Tesseract OCR: https://github.com/tesseract-ocr/tesseract
  - Poppler: requerido por pdf2image para convertir PDF a imágenes

Instalación en Windows:
  - Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
  - Poppler: https://github.com/oschwartz10612/poppler-windows/releases

Instalación en Mac:
  brew install tesseract poppler

Instalación en Linux:
  sudo apt install tesseract-ocr poppler-utils
"""

import pytesseract
from pdf2image import convert_from_path


def extract_text_with_ocr(pdf_path: str, language: str = "spa") -> str:
    """
    Convierte cada página del PDF en imagen y extrae su texto con OCR.

    Args:
        pdf_path: Ruta al archivo PDF escaneado.
        language: Idioma para el OCR. "spa" = español, "eng" = inglés.
                  Se puede combinar: "spa+eng" para ambos.

    Returns:
        Texto extraído mediante OCR, con separadores por página.

    Raises:
        FileNotFoundError: Si el archivo PDF no existe.
        RuntimeError: Si Tesseract no está instalado en el sistema.
    """
    try:
        pages = convert_from_path(pdf_path)
    except Exception as e:
        raise RuntimeError(
            f"No se pudo convertir el PDF a imágenes. "
            f"Asegurate de tener Poppler instalado. Error: {e}"
        )

    full_text = ""

    for i, page_image in enumerate(pages):
        try:
            page_text = pytesseract.image_to_string(page_image, lang=language)
        except pytesseract.TesseractNotFoundError:
            raise RuntimeError(
                "Tesseract no está instalado o no se encuentra en el PATH. "
                "Instalalo desde: https://github.com/UB-Mannheim/tesseract/wiki"
            )

        if page_text.strip():
            full_text += f"--- Página {i + 1} ---\n"
            full_text += page_text.strip() + "\n\n"

    return full_text
