"""
app/text_structure.py
---------------------
Detección y preservación de estructura en texto extraído de PDFs.

Detecta:
  - Títulos y subtítulos (líneas cortas, en mayúsculas, o con fuente grande)
  - Viñetas y listas (líneas que empiezan con -, •, *, o número+punto)
  - Párrafos separados (bloques separados por líneas vacías)

La estructura detectada se expresa en formato Markdown para que sea
legible y útil para el modelo de IA al generar el resumen. (Issue #16)
"""

import re


def detect_structure(text: str) -> str:
    """
    Analiza el texto plano extraído de un PDF y devuelve el mismo texto
    con su estructura preservada en formato Markdown.

    Args:
        text: Texto plano extraído del PDF.

    Returns:
        Texto con estructura Markdown (títulos, listas, párrafos).
    """
    if not text or not text.strip():
        return text

    lines = text.splitlines()
    structured_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Línea vacía → separador de párrafo
        if not stripped:
            structured_lines.append("")
            i += 1
            continue

        # Detección de viñetas/listas
        if _is_bullet(stripped):
            structured_lines.append(_format_bullet(stripped))
            i += 1
            continue

        # Detección de títulos
        if _is_title(stripped, lines, i):
            structured_lines.append(_format_title(stripped, lines, i))
            i += 1
            continue

        # Línea de párrafo normal
        structured_lines.append(stripped)
        i += 1

    return "\n".join(structured_lines)


# ------------------------------------------------------------------ #
# Funciones auxiliares privadas
# ------------------------------------------------------------------ #

def _is_bullet(line: str) -> bool:
    """Detecta si una línea es una viñeta o ítem de lista."""
    bullet_patterns = [
        r"^[-•·*]\s+.+",        # - texto / • texto / * texto
        r"^\d+[\.\)]\s+.+",     # 1. texto / 1) texto
        r"^[a-zA-Z][\.\)]\s+.+", # a. texto / a) texto
    ]
    return any(re.match(p, line) for p in bullet_patterns)


def _is_title(line: str, lines: list[str], index: int) -> bool:
    """
    Detecta si una línea es un título o subtítulo usando heurísticas:
      - Es corta (menos de 80 caracteres)
      - Está en MAYÚSCULAS completas
      - O es la primera línea de un bloque (viene después de línea vacía)
        y la siguiente línea también tiene contenido
    """
    if len(line) > 80:
        return False

    # Título en mayúsculas (y tiene más de 2 palabras o caracteres)
    if line.isupper() and len(line) > 3:
        return True

    # Línea que termina sin punto (típico de títulos) y es corta
    # y viene después de una línea vacía o es la primera línea
    prev_is_empty = index == 0 or not lines[index - 1].strip()
    next_has_content = (index + 1 < len(lines)) and lines[index + 1].strip()

    if prev_is_empty and next_has_content and not line.endswith(".") and len(line) < 60:
        return True

    return False


def _format_title(line: str, lines: list[str], index: int) -> str:
    """
    Formatea un título con el nivel Markdown adecuado.
    Si está en mayúsculas → ## (título principal)
    Si no → ### (subtítulo)
    """
    if line.isupper():
        return f"## {line.title()}"
    return f"### {line}"


def _format_bullet(line: str) -> str:
    """Normaliza viñetas al formato Markdown estándar con guión."""
    # Reemplaza •, ·, * al inicio por -
    normalized = re.sub(r"^[•·*]\s+", "- ", line)
    # Normaliza listas numeradas: deja como están (1. texto)
    return normalized
