from django.db import models
from django.utils import timezone
import uuid


class Summary(models.Model):
    """Model para almacenar resúmenes de PDFs generados"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_filename = models.CharField(max_length=255)
    summary_text = models.TextField()
    extracted_text = models.TextField(blank=True)  # Primeros 1000 caracteres
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Summary"
        verbose_name_plural = "Summaries"

    def __str__(self):
        return (
            f"{self.original_filename} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )

    def save(self, *args, **kwargs):
        # Limitar extracted_text a 1000 caracteres
        if len(self.extracted_text) > 1000:
            self.extracted_text = self.extracted_text[:1000]
        super().save(*args, **kwargs)
