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
