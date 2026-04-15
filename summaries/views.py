"""Vistas Django para procesamiento de resúmenes"""

import json
import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Summary
from .services import SummaryService


logger = logging.getLogger(__name__)


def index(request):
    """Página principal con interfaz para upload de PDF"""
    return render(request, "summaries/index.html")


@require_http_methods(["POST"])
@csrf_exempt
def summarize_pdf(request):
    """
    Endpoint para subir un PDF y generar resumen

    Accepts: multipart/form-data con field 'file'
    Returns: JSON con id, filename, summary_text, created_at
    """
    try:
        # Validar que se envió un archivo
        if "file" not in request.FILES:
            return JsonResponse({"error": "No file provided"}, status=400)

        uploaded_file = request.FILES["file"]

        # Validar que es PDF
        if not uploaded_file.name.lower().endswith(".pdf"):
            return JsonResponse({"error": "Only PDF files are allowed"}, status=400)

        # Validar que no está vacío
        if uploaded_file.size == 0:
            return JsonResponse({"error": "File is empty"}, status=400)

        # Leer contenido del archivo
        file_content = uploaded_file.read()

        # Generar resumen
        service = SummaryService()
        summary_data = service.create_summary(file_content, uploaded_file.name)

        # Guardar en la base de datos
        summary = Summary.objects.create(**summary_data)

        return JsonResponse(
            {
                "id": str(summary.id),
                "original_filename": summary.original_filename,
                "summary_text": summary.summary_text,
                "created_at": summary.created_at.isoformat(),
            }
        )

    except ValueError as e:
        return JsonResponse({"error": f"Invalid PDF file: {str(e)}"}, status=400)
    except Exception as e:
        logger.exception("Error generating summary")
        return JsonResponse({"error": f"Error processing file: {str(e)}"}, status=500)


@require_http_methods(["GET"])
def list_summaries(request):
    """
    Lista todos los resúmenes con paginación

    Query params:
        - limit: número de items por página (default: 100)
        - page: número de página (default: 1)

    Returns: JSON con lista de resúmenes y total
    """
    try:
        limit = int(request.GET.get("limit", 100))
        page = int(request.GET.get("page", 1))

        # Limitar a máximo 100 items por página
        limit = min(limit, 100)

        # Obtener resúmenes ordenados por fecha descendente
        summaries_qs = Summary.objects.all().order_by("-created_at")

        # Paginar
        paginator = Paginator(summaries_qs, limit)
        summaries_page = paginator.get_page(page)

        summaries_data = [
            {
                "id": str(s.id),
                "original_filename": s.original_filename,
                "summary_text": s.summary_text,
                "created_at": s.created_at.isoformat(),
            }
            for s in summaries_page
        ]

        return JsonResponse(
            {
                "summaries": summaries_data,
                "total": paginator.count,
                "page": page,
                "total_pages": paginator.num_pages,
            }
        )

    except Exception as e:
        logger.exception("Error listing summaries")
        return JsonResponse(
            {"error": f"Error fetching summaries: {str(e)}"}, status=500
        )


@require_http_methods(["GET"])
def get_summary(request, summary_id):
    """
    Obtiene un resumen específico por ID

    Returns: JSON con datos del resumen o 404 si no existe
    """
    try:
        summary = get_object_or_404(Summary, id=summary_id)

        return JsonResponse(
            {
                "id": str(summary.id),
                "original_filename": summary.original_filename,
                "summary_text": summary.summary_text,
                "extracted_text": summary.extracted_text,
                "created_at": summary.created_at.isoformat(),
            }
        )

    except Summary.DoesNotExist:
        return JsonResponse({"error": "Summary not found"}, status=404)
    except Exception as e:
        logger.exception("Error fetching summary")
        return JsonResponse({"error": f"Error fetching summary: {str(e)}"}, status=500)


@require_http_methods(["GET"])
def health_check(request):
    """
    Verifica si el servicio y sus dependencias están disponibles

    Returns: JSON con estado de salud
    """
    try:
        service = SummaryService()
        generator_available = service.summary_generator.health_check()

        status = "healthy" if generator_available else "degraded"

        return JsonResponse(
            {"status": status, "generator_available": generator_available}
        )

    except Exception as e:
        logger.exception("Error in health check")
        return JsonResponse(
            {"status": "degraded", "generator_available": False, "error": str(e)}
        )
