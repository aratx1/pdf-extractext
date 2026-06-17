"""
app/cache.py
------------
Caché de resúmenes basado en hash del texto extraído del PDF.

Si el mismo PDF (o uno con el mismo contenido) ya fue procesado antes,
se devuelve el resumen guardado sin volver a llamar a la API.
Esto ahorra llamadas a la API y mejora la velocidad. (Issue #11)
"""

import hashlib
import json
import os

CACHE_FILE = "cache.json"


def _get_text_hash(text: str) -> str:
    """Genera un hash SHA256 del texto extraído."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _load_cache() -> dict:
    """Carga el caché desde el archivo JSON. Si no existe, devuelve vacío."""
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_cache(cache: dict) -> None:
    """Guarda el caché en el archivo JSON."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_cached_summary(text: str) -> str | None:
    """
    Busca en el caché si ya existe un resumen para este texto.

    Args:
        text: El texto extraído del PDF.

    Returns:
        El resumen guardado si existe, o None si no hay caché para este texto.
    """
    text_hash = _get_text_hash(text)
    cache = _load_cache()
    return cache.get(text_hash, None)


def save_summary_to_cache(text: str, summary: str) -> None:
    """
    Guarda un resumen en el caché asociado al hash del texto.

    Args:
        text: El texto extraído del PDF (se usa para generar el hash).
        summary: El resumen generado por la API que queremos guardar.
    """
    text_hash = _get_text_hash(text)
    cache = _load_cache()
    cache[text_hash] = summary
    _save_cache(cache)
