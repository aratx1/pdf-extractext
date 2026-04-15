# Guía Paso a Paso: Migración de FastAPI a Django

Esta guía detalla exactamente qué se hizo para migrar el proyecto PDF Summarizer de FastAPI a Django.

---

## Paso 1: Análisis del Proyecto Original

### Qué se encontró:

El proyecto estaba organizado en la carpeta `app/` con Clean Architecture:

```
app/
├── core/              → Configuración (Settings)
├── application/       → Lógica de negocio
│   ├── interfaces/    → Contratos (abstractos)
│   └── services/      → Servicios (PDFService, SummaryService)
├── infrastructure/    → Implementaciones externas
│   ├── external/      → API clients (Nvidia)
│   ├── file_storage/  → File handler
│   └── repositories/  → Repositories (en memoria)
└── presentation/      → API REST
    ├── routers/       → Endpoints FastAPI
    ├── schemas/       → Modelos Pydantic
    └── templates/     → HTML web
```

### Análisis de dependencias:

**Instaladas:**
- FastAPI
- Pydantic
- pypdf
- httpx
- aiofiles

**Necesarias para Django:**
- django
- pypdf (✓ ya está)
- httpx (✓ ya está)
- python-dotenv (✨ faltaba)

---

## Paso 2: Crear Estructura Django

### Crear carpeta `summaries/`:

```bash
mkdir summaries
```

### Crear archivos base:

```
summaries/
├── __init__.py          (vacío)
├── apps.py              (configuración)
├── admin.py             (administrador)
├── models.py            (modelos)
├── views.py             (vistas/endpoints)
├── urls.py              (rutas)
├── services.py          (servicios)
├── tests.py             (tests)
├── migrations/
│   ├── __init__.py      (vacío)
│   └── 0001_initial.py  (migración)
└── templates/summaries/
    └── index.html       (template)
```

---

## Paso 3: Crear el Modelo Django

### Archivo: `summaries/models.py`

**Conceptos clave:**

1. **UUID como primary_key**: Mantener IDs globalmente únicos como en FastAPI
2. **DateTimeField**: Django maneja automáticamente created_at
3. **TextField**: Para textos largos (summary y extracted)
4. **CharField**: Para strings cortos (filename)

```python
from django.db import models
import uuid

class Summary(models.Model):
    # ID único global
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Datos del resumen
    original_filename = models.CharField(max_length=255)
    summary_text = models.TextField()
    extracted_text = models.TextField(blank=True)
    
    # Timestamp automático
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']  # Ordenar por fecha descendente
        verbose_name = 'Summary'
        verbose_name_plural = 'Summaries'
```

**Cambios respecto a FastAPI:**

| Aspecto | FastAPI | Django |
|--------|---------|--------|
| Definición | Dataclass con `@dataclass` | Modelo con herencia de `models.Model` |
| ID | Manual con UUID() | Automático con default=uuid.uuid4 |
| Timestamps | Manual con datetime.now() | Automático con auto_now_add=True |
| Persistencia | Manual (diccionario) | Automática (BD) |
| Validación | Pydantic | Django validators |

---

## Paso 4: Migrar Servicios

### Archivo: `summaries/services.py`

#### 4.1 PDFService (Sin cambios)

```python
class PDFService:
    @staticmethod
    def extract_text(file_content: bytes, filename: str) -> ExtractedPDF:
        # Se copió tal cual de FastAPI
        # La lógica de extracción es independiente del framework
```

**Por qué no cambió:**
- Es lógica pura (toma bytes, retorna datos)
- No depende de FastAPI
- Puede reutilizarse en cualquier framework

#### 4.2 NvidiaAIProvider (Adaptado)

**Cambio 1: Cargar config desde Django settings**

```python
# Antes (FastAPI):
from app.core import get_settings
api_key = get_settings().nvidia_api_key

# Después (Django):
from django.conf import settings
api_key = settings.NVIDIA_API_KEY
```

**Cambio 2: El resto del código es igual**

La llamada a la API Nvidia es idéntica, solo cambia dónde se obtienen las credenciales.

#### 4.3 SummaryService (Adaptado)

**Cambio 1: Crear registro en BD en vez de en memoria**

```python
# Antes (FastAPI):
repository.save(summary)  # En diccionario

# Después (Django):
Summary.objects.create(**summary_data)  # En base de datos
```

**Cambio 2: Retornar diccionario en vez de objeto**

```python
# Antes (FastAPI):
return summary: Summary  # Retorna objeto

# Después (Django):
return {
    'original_filename': filename,
    'summary_text': ai_response.content,
    'extracted_text': extracted.text[:1000],
}
```

---

## Paso 5: Crear Vistas Django

### Archivo: `summaries/views.py`

#### 5.1 Vista: Index

```python
def index(request):
    """Página principal con formulario"""
    return render(request, 'summaries/index.html')
```

**Cambio respecto a FastAPI:**
- FastAPI: Retorna HTML como string
- Django: Renderiza template desde carpeta templates/

#### 5.2 Vista: Generar Resumen

**FastAPI:**
```python
@app.post("/api/summarize")
async def summarize_pdf(file: UploadFile) -> SummaryResponse:
    # Validaciones
    # Procesamiento
    # Return JSON
```

**Django:**
```python
@require_http_methods(["POST"])
@csrf_exempt
def summarize_pdf(request):
    # Validaciones idénticas
    # Procesamiento idéntico
    # Return JsonResponse (JSON)
```

**Cambios:**
- Sin `async` (Django es sincrónico por defecto)
- Usar `request.FILES` en vez de `UploadFile`
- Retornar `JsonResponse` en vez de JSON dict
- `@csrf_exempt` para desactivar protección CSRF en API

#### 5.3 Vista: Listar Resúmenes

**FastAPI:**
```python
summaries = repository.get_all(limit=limit)
return {'summaries': summaries, 'total': len(summaries)}
```

**Django:**
```python
summaries_qs = Summary.objects.all().order_by('-created_at')
paginator = Paginator(summaries_qs, limit)
summaries_page = paginator.get_page(page)
```

**Cambios:**
- Usar ORM queries en vez de métodos de repository
- Uso de Paginator para paginación automática
- Ordenar con ORM en vez de en Python

---

## Paso 6: Crear URLs

### Archivo: `summaries/urls.py`

```python
from django.urls import path
from . import views

app_name = 'summaries'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/summarize/', views.summarize_pdf, name='summarize'),
    path('api/summaries/', views.list_summaries, name='list'),
    path('api/summaries/<uuid:summary_id>/', views.get_summary, name='detail'),
    path('api/health/', views.health_check, name='health'),
]
```

**Incluir en config/urls.py:**
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('summaries.urls')),  # ✨ Nueva línea
]
```

---

## Paso 7: Configurar Django Settings

### Archivo: `config/settings.py`

#### 7.1 Agregar app a INSTALLED_APPS:

```python
INSTALLED_APPS = [
    # ... apps por defecto ...
    'summaries',  # ✨ Nueva
]
```

#### 7.2 Cargar variables de entorno:

```python
import os
from dotenv import load_dotenv

load_dotenv()
```

#### 7.3 Agregar configuración de IA:

```python
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')
NVIDIA_API_URL = os.getenv('NVIDIA_API_URL', 'https://integrate.api.nvidia.com/v1')
AI_MODEL = os.getenv('AI_MODEL', 'meta/llama-3.2-90b-vision-instruct')
```

---

## Paso 8: Crear Migraciones

### Archivo: `summaries/migrations/0001_initial.py`

```python
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    
    operations = [
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)),
                ('original_filename', models.CharField(max_length=255)),
                ('summary_text', models.TextField()),
                ('extracted_text', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Summary',
                'verbose_name_plural': 'Summaries',
                'ordering': ['-created_at'],
            },
        ),
    ]
```

**Ejecutar:**
```bash
python manage.py migrate
```

---

## Paso 9: Configurar Admin

### Archivo: `summaries/admin.py`

```python
from django.contrib import admin
from .models import Summary

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('original_filename', 'summary_text')
    readonly_fields = ('id', 'created_at')
```

**Resultado:**
- Panel admin en `/admin/`
- Listar, crear, editar, eliminar resúmenes
- Búsqueda por nombre y texto
- Filtro por fecha

---

## Paso 10: Migrar Template HTML

### Cambios en `summaries/templates/summaries/index.html`:

#### 10.1 Agregar CSRF token

```html
<form id="upload-form">
    {% csrf_token %}  <!-- ✨ Nueva línea -->
    <input type="file" id="pdf-input" accept=".pdf">
    <button type="submit">Generate Summary</button>
</form>
```

#### 10.2 Actualizar rutas en JavaScript

```javascript
// Antes: /api/summarize
// Después: /api/summarize/ (trailing slash)

// Antes
const response = await fetch('/api/summarize', {

// Después
const response = await fetch('/api/summarize/', {
```

#### 10.3 Actualizar manejo de errores

```javascript
// Antes: error.detail
// Después: error.error

if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to generate summary');
    //                     ↑ Django retorna 'error' no 'detail'
}
```

---

## Paso 11: Actualizar Dependencias

### Archivo: `pyproject.toml`

```toml
[project]
dependencies = [
    "django>=5.2.13",
    "pypdf>=4.0.0",       # ✨ Mantener
    "httpx>=0.24.0",      # ✨ Mantener
    "python-dotenv>=1.0.0", # ✨ Nueva
]
```

### Instalar con UV:

```bash
uv add python-dotenv pypdf httpx
```

---

## Paso 12: Crear Archivo .env

### Archivo: `.env`

```env
NVIDIA_API_KEY=your-nvidia-api-key-here
NVIDIA_API_URL=https://integrate.api.nvidia.com/v1
AI_MODEL=meta/llama-3.2-90b-vision-instruct
```

**Importante:** No commitear este archivo (agregado a .gitignore)

---

## Paso 13: Actualizar .gitignore

### Cambios realizados:

```gitignore
# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/staticfiles/           # ✨ Nuevo
/media/                 # ✨ Nuevo
/uploads/               # ✨ Nuevo

# Environments
.env                    # ✨ Mantener
.env.local              # ✨ Nuevo
.env.*.local            # ✨ Nuevo
```

---

## Paso 14: Validar y Ejecutar

### Verificar sintaxis:

```bash
python -m py_compile summaries/*.py
```

### Verificar configuración de Django:

```bash
python manage.py check
```

**Salida esperada:**
```
System check identified no issues (0 silenced).
```

### Ejecutar migraciones:

```bash
python manage.py migrate
```

**Salida esperada:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, summaries
Running migrations:
  Applying summaries.0001_initial... OK
```

### Iniciar servidor:

```bash
python manage.py runserver
```

**Salida esperada:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Acceder a la aplicación:

- **Web:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/
- **API:** http://127.0.0.1:8000/api/summaries/

---

## Resumen de cambios

### Por categoría:

| Categoría | FastAPI | Django | Cambio |
|-----------|---------|--------|--------|
| **Framework** | FastAPI | Django | Completo |
| **ORM** | En memoria | Django ORM | Completo |
| **Modelos** | Pydantic dataclass | Django model | Completo |
| **Vistas** | Decoradores @app | Funciones def | Nuevo sistema |
| **Rutas** | include_router | URLconf | Nuevo sistema |
| **Templates** | String HTML | Jinja2 templates | Carpeta templates/ |
| **Configuración** | app/core | config/settings.py | Centralizado |
| **Admin** | Ninguno | Django admin | Nuevo |
| **BD** | En memoria | SQLite | Persistencia |
| **Servicios** | Igual | Igual | Reutilización |

### Linaje de cambio:

```
FastAPI (async)           →  Django (sync)
├─ app/main.py           →  config/urls.py + summaries/views.py
├─ app/core/             →  config/settings.py
├─ Pydantic models       →  Django models
├─ Routers FastAPI       →  Views + URLs
├─ En memoria            →  SQLite database
├─ Schemas Pydantic      →  JSON directo
└─ Templates strings     →  Jinja2 templates
```

---

## Archivos finales

### Creados (13 archivos):

1. `summaries/__init__.py`
2. `summaries/apps.py`
3. `summaries/admin.py`
4. `summaries/models.py`
5. `summaries/views.py`
6. `summaries/urls.py`
7. `summaries/services.py`
8. `summaries/tests.py`
9. `summaries/migrations/__init__.py`
10. `summaries/migrations/0001_initial.py`
11. `summaries/templates/summaries/index.html`
12. `.env`
13. `docs/migracion_fastapi_a_django.md`

### Modificados (5 archivos):

1. `config/settings.py` - +35 líneas
2. `config/urls.py` - +1 línea
3. `pyproject.toml` - +2 dependencias
4. `.gitignore` - +8 líneas
5. `README.md` - Reescrito

### Total:

- **Líneas de código nuevas:** ~700 líneas
- **Tiempo estimado:** 1 hora
- **Complejidad:** Media
- **Riesgos:** Bajos

---

**Fin de la guía paso a paso**
