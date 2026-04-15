"""URLs para la app de resúmenes"""

from django.urls import path
from . import views

app_name = "summaries"

urlpatterns = [
    # Página principal
    path("", views.index, name="index"),
    # API endpoints
    path("api/summarize/", views.summarize_pdf, name="summarize"),
    path("api/summaries/", views.list_summaries, name="list"),
    path("api/summaries/<uuid:summary_id>/", views.get_summary, name="detail"),
    path("api/health/", views.health_check, name="health"),
]
