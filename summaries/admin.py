from django.contrib import admin
from .models import Summary


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ("original_filename", "created_at")
    list_filter = ("created_at",)
    search_fields = ("original_filename", "summary_text")
    readonly_fields = ("id", "created_at")
    fieldsets = (
        ("Información del Archivo", {"fields": ("id", "original_filename")}),
        ("Contenido", {"fields": ("summary_text", "extracted_text")}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
