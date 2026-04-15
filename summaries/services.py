"""Servicios para procesamiento de PDFs y generación de resúmenes"""

from dataclasses import dataclass
from typing import Optional
from pypdf import PdfReader


@dataclass
class ExtractedPDF:
    """Resultado de extracción de un PDF"""

    filename: str
    text: str
    page_count: int
    character_count: int


@dataclass
class AIResponse:
    """Respuesta del proveedor de IA"""

    content: str
    model: str
    tokens_used: Optional[int] = None


class PDFService:
    """Servicio para extraer texto de archivos PDF"""

    @staticmethod
    def extract_text(file_content: bytes, filename: str) -> ExtractedPDF:
        """
        Extrae texto de un archivo PDF

        Args:
            file_content: Contenido del archivo en bytes
            filename: Nombre del archivo

        Returns:
            ExtractedPDF con texto extraído y estadísticas
        """
        pdf_reader = PdfReader(file_content)
        text_parts = []

        for page in pdf_reader.pages:
            text_parts.append(page.extract_text())

        full_text = "\n\n".join(text_parts)

        return ExtractedPDF(
            filename=filename,
            text=full_text,
            page_count=len(pdf_reader.pages),
            character_count=len(full_text),
        )


class SimpleSummaryGenerator:
    """Generador de resúmenes simple basado en frecuencia de palabras"""

    @staticmethod
    def generate_summary(text: str, max_length: int = 500) -> AIResponse:
        """
        Genera un resumen simple del texto basado en frecuencia de palabras

        Args:
            text: Texto a resumir
            max_length: Longitud máxima del resumen en palabras

        Returns:
            AIResponse con el resumen generado
        """
        # Dividir en oraciones
        sentences = (
            text.replace(".", ".\n").replace("?", "?\n").replace("!", "!\n").split("\n")
        )
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return AIResponse(
                content="No se pudo generar resumen: archivo vacío",
                model="simple-frequency",
                tokens_used=None,
            )

        # Calcular puntuación de cada oración basada en palabras frecuentes
        words = text.lower().split()
        word_freq = {}
        for word in words:
            # Limpiar palabra
            word = "".join(c for c in word if c.isalnum())
            if len(word) > 3:  # Solo palabras > 3 caracteres
                word_freq[word] = word_freq.get(word, 0) + 1

        # Puntuar oraciones
        scored_sentences = []
        for sentence in sentences:
            score = sum(word_freq.get(word.lower(), 0) for word in sentence.split())
            scored_sentences.append((score, sentence))

        # Ordenar por puntuación y tomar las mejores
        scored_sentences.sort(reverse=True)
        summary_sentences = sorted(
            scored_sentences[:3], key=lambda x: sentences.index(x[1])
        )
        summary = " ".join([s[1] for s in summary_sentences])

        # Limitar a max_length palabras
        summary_words = summary.split()
        if len(summary_words) > max_length:
            summary = " ".join(summary_words[:max_length]) + "..."

        return AIResponse(
            content=summary, model="simple-frequency", tokens_used=len(summary.split())
        )

    @staticmethod
    def health_check() -> bool:
        """
        Verifica si el generador está disponible

        Returns:
            Siempre True (no tiene dependencias externas)
        """
        return True


class SummaryService:
    """Servicio de orquestación para generación de resúmenes"""

    def __init__(self):
        """Inicializa con las dependencias necesarias"""
        self.pdf_service = PDFService()
        self.summary_generator = SimpleSummaryGenerator()

    def create_summary(self, file_content: bytes, filename: str) -> dict:
        """
        Crea un resumen a partir de un PDF

        Args:
            file_content: Contenido del archivo PDF
            filename: Nombre del archivo

        Returns:
            Diccionario con los datos del resumen generado

        Raises:
            Exception si ocurre error en extracción o generación
        """
        # Extraer texto del PDF
        extracted = self.pdf_service.extract_text(file_content, filename)

        # Generar resumen
        ai_response = self.summary_generator.generate_summary(extracted.text)

        return {
            "original_filename": filename,
            "summary_text": ai_response.content,
            "extracted_text": extracted.text[:1000],  # Limitar a 1000 caracteres
        }
