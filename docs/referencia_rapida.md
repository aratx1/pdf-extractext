# Guía de Referencia Rápida - Migración Django

Referencia rápida para acceder a comandos, archivos y conceptos clave de la migración.

---

## 🚀 Comandos Esenciales

### Ejecutar aplicación

```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# Acceder a la app
http://127.0.0.1:8000/
```

### Base de datos

```bash
# Ver migraciones pendientes
python manage.py showmigrations

# Aplicar migraciones
python manage.py migrate

# Crear nueva migración
python manage.py makemigrations

# Revisar cambios de migración
python manage.py migrate --plan
```

### Admin

```bash
# Crear superusuario
python manage.py createsuperuser

# Acceder a admin
http://127.0.0.1:8000/admin/
```

### Testing

```bash
# Ejecutar tests
python manage.py test

# Ejecutar con pytest
pytest

# Con cobertura
pytest --cov=summaries
```

### Utilidades

```bash
# Revisar configuración
python manage.py check

# Mostrar SQL de una query
python manage.py sqlshell

# Generar requirements.txt
pip freeze > requirements.txt
```

---

## 📁 Estructura de Archivos Clave

### App Django (`summaries/`)

```
summaries/
├── models.py           # Define tabla Summary
├── views.py            # Endpoints API (5 vistas)
├── urls.py             # Rutas de la app
├── services.py         # Lógica de negocio
├── admin.py            # Panel admin
├── forms.py            # Formularios (no usados)
├── tests.py            # Tests
└── migrations/
    ├── __init__.py
    └── 0001_initial.py # Primera migración
```

### Configuración (`config/`)

```
config/
├── settings.py         # Configuración principal (MODIFICADO)
├── urls.py             # Rutas globales (MODIFICADO)
├── asgi.py             # ASGI app
└── wsgi.py             # WSGI app
```

### Root

```
.env                     # Variables de entorno (NO COMMITEAR)
.gitignore              # Ignorados de git (MODIFICADO)
README.md               # Documentación (REESCRITO)
pyproject.toml          # Dependencias (MODIFICADO)
manage.py               # CLI de Django
db.sqlite3              # Base de datos (NO COMMITEAR)
```

---

## 🔑 Conceptos Clave

### Modelo Summary

```python
# Ubicación: summaries/models.py

class Summary(models.Model):
    id = UUIDField(primary_key=True, default=uuid4)
    original_filename = CharField(max_length=255)
    summary_text = TextField()
    extracted_text = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
```

**Campos:**
- `id`: UUID único
- `original_filename`: Nombre del PDF
- `summary_text`: Resumen generado
- `extracted_text`: Primeros 1000 caracteres
- `created_at`: Fecha automática

### Vistas (Endpoints)

| Nombre | Ruta | Método | Función |
|--------|------|--------|---------|
| `index` | `/` | GET | Página principal |
| `summarize_pdf` | `/api/summarize/` | POST | Generar resumen |
| `list_summaries` | `/api/summaries/` | GET | Listar resúmenes |
| `get_summary` | `/api/summaries/<id>/` | GET | Obtener uno |
| `health_check` | `/api/health/` | GET | Estado de IA |

### Servicios

```python
# Ubicación: summaries/services.py

PDFService              # Extrae texto de PDF
NvidiaAIProvider        # Llama API Nvidia
SummaryService          # Orquesta todo
```

---

## 📝 Endpoints API

### 1. Generar Resumen

```bash
# Request
curl -X POST http://127.0.0.1:8000/api/summarize/ \
  -F "file=@documento.pdf"

# Response (200 OK)
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "original_filename": "documento.pdf",
  "summary_text": "Resumen del documento...",
  "created_at": "2026-04-15T23:40:00Z"
}

# Error (400 Bad Request)
{
  "error": "Only PDF files are allowed"
}
```

### 2. Listar Resúmenes

```bash
# Request
curl http://127.0.0.1:8000/api/summaries/

# Response (200 OK)
{
  "summaries": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "original_filename": "documento.pdf",
      "summary_text": "Resumen...",
      "created_at": "2026-04-15T23:40:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "total_pages": 1
}
```

### 3. Obtener Un Resumen

```bash
# Request
curl http://127.0.0.1:8000/api/summaries/550e8400-e29b-41d4-a716-446655440000/

# Response (200 OK)
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "original_filename": "documento.pdf",
  "summary_text": "Resumen del documento...",
  "extracted_text": "Primeros 1000 caracteres del PDF...",
  "created_at": "2026-04-15T23:40:00Z"
}

# Error (404 Not Found)
{
  "error": "Summary not found"
}
```

### 4. Health Check

```bash
# Request
curl http://127.0.0.1:8000/api/health/

# Response (200 OK)
{
  "status": "healthy",
  "ai_provider_available": true
}

# O si hay error
{
  "status": "degraded",
  "ai_provider_available": false,
  "error": "Connection refused"
}
```

---

## 🔧 Variables de Entorno

### Archivo `.env`

```env
# API de Nvidia
NVIDIA_API_KEY=tu-api-key-aqui
NVIDIA_API_URL=https://integrate.api.nvidia.com/v1
AI_MODEL=meta/llama-3.2-90b-vision-instruct
```

**Obtener API key:**
1. Ir a https://build.nvidia.com/
2. Crear cuenta
3. Generar API key
4. Copiar a `.env`

**No commitear:** `.env` está en `.gitignore`

---

## 🗂️ Cambios Clave por Archivo

### `config/settings.py`

**Agregado:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

INSTALLED_APPS = [
    ...
    'summaries',  # ← Nueva
]

NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')
NVIDIA_API_URL = os.getenv('NVIDIA_API_URL', '...')
AI_MODEL = os.getenv('AI_MODEL', '...')
```

### `config/urls.py`

**Cambio:**
```python
# Antes:
urlpatterns = [
    path('admin/', admin.site.urls),
]

# Después:
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('summaries.urls')),  # ← Nuevo
]
```

### `pyproject.toml`

**Dependencias agregadas:**
```toml
dependencies = [
    "django>=5.2.13",
    "pypdf>=4.0.0",
    "httpx>=0.24.0",
    "python-dotenv>=1.0.0",  # ← Nuevo
]
```

### `.gitignore`

**Agregado:**
```gitignore
/staticfiles/
/media/
/uploads/
.env.local
.env.*.local
```

---

## 🐛 Troubleshooting

### Error: "No module named dotenv"

```bash
# Solución
uv add python-dotenv
# O
pip install python-dotenv
```

### Error: "NVIDIA_API_KEY not configured"

```bash
# Solución
# 1. Crear .env
# 2. Agregar: NVIDIA_API_KEY=tu-clave
# 3. Reiniciar servidor
```

### Error: "ModuleNotFoundError: No module named 'summaries'"

```bash
# Solución
# Asegurar que 'summaries' está en INSTALLED_APPS en settings.py
# python manage.py check
```

### Error: "404 on /api/summarize/"

```bash
# Solución
# 1. Verificar que config/urls.py incluye summaries.urls
# 2. Ejecutar: python manage.py check
# 3. Reiniciar servidor
```

### Error: "Trailing slash required"

```bash
# Cambio en Django 3+
# Todas las rutas requieren trailing slash

# FastAPI: /api/summarize
# Django:  /api/summarize/  ← Nota el /
```

---

## 📊 Comparación Rápida

### Operación: Listar elementos

```python
# FastAPI (antiguo)
def get_all(self, limit: int = 100) -> list[Summary]:
    return list(self._storage.values())[:limit]

# Django (nuevo)
summaries = Summary.objects.all()[:limit]
# O con paginación
from django.core.paginator import Paginator
paginator = Paginator(Summary.objects.all(), limit)
page = paginator.get_page(1)
```

### Operación: Crear elemento

```python
# FastAPI (antiguo)
def save(self, summary: Summary) -> Summary:
    summary.id = uuid4()
    self._storage[summary.id] = summary
    return summary

# Django (nuevo)
summary = Summary.objects.create(
    original_filename=filename,
    summary_text=text
)
```

### Operación: Obtener por ID

```python
# FastAPI (antiguo)
def get_by_id(self, summary_id: UUID) -> Summary | None:
    return self._storage.get(summary_id)

# Django (nuevo)
try:
    summary = Summary.objects.get(id=summary_id)
except Summary.DoesNotExist:
    summary = None
```

---

## 🎯 Workflow Típico

### 1. Desarrollo

```bash
# Terminal 1: Servidor
python manage.py runserver

# Terminal 2: Tests (si aplica)
pytest -v

# Acceder a:
# - App: http://127.0.0.1:8000/
# - Admin: http://127.0.0.1:8000/admin/
# - API: http://127.0.0.1:8000/api/
```

### 2. Cambio en Modelo

```bash
# 1. Editar summaries/models.py
# 2. Crear migración
python manage.py makemigrations

# 3. Revisar migración
cat summaries/migrations/000X_auto_FECHA.py

# 4. Aplicar
python manage.py migrate

# 5. Restart servidor
# (Presionar Ctrl+C y repetir python manage.py runserver)
```

### 3. Nuevo Endpoint

```bash
# 1. Agregar vista en summaries/views.py
def my_view(request):
    return JsonResponse({"data": "..."})

# 2. Agregar URL en summaries/urls.py
path('api/my-endpoint/', views.my_view)

# 3. Restart servidor

# 4. Probar
curl http://127.0.0.1:8000/api/my-endpoint/
```

---

## 📚 Recursos

### Documentación oficial

- **Django:** https://docs.djangoproject.com/
- **Django ORM:** https://docs.djangoproject.com/en/5.2/topics/db/models/
- **Django Views:** https://docs.djangoproject.com/en/5.2/topics/http/views/

### Cheat sheets útiles

```bash
# Queries ORM
Model.objects.all()
Model.objects.filter(field=value)
Model.objects.get(id=id)
Model.objects.create(field=value)
Model.objects.update(field=value)
Model.objects.delete()

# Agregaciones
Model.objects.count()
Model.objects.order_by('-field')
Model.objects.distinct()
Model.objects.values('field')

# Relaciones
Model.objects.select_related('foreign_key')
Model.objects.prefetch_related('many_to_many')
```

---

## ✅ Checklist Post-Migración

- [x] App Django creada (`summaries/`)
- [x] Modelo Summary funcionando
- [x] Vistas API funcionando
- [x] Admin panel funcionando
- [x] Template HTML migrante
- [x] BD creada y migraciones aplicadas
- [x] Variables de entorno configuradas
- [x] `.gitignore` actualizado
- [x] Dependencias instaladas
- [x] Tests de endpoints (manual)

### Para futuro:

- [ ] Escribir tests unitarios
- [ ] Documentar API (Swagger)
- [ ] Configurar logging
- [ ] Optimizar queries
- [ ] Agregar autenticación

---

**Última actualización:** 15 de abril de 2026
