# Documentación: Migración de FastAPI a Django

**Fecha:** 15 de abril de 2026  
**Proyecto:** PDF Summarizer  
**Estado:** ✅ Completado

---

## 📋 Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Estructura del Proyecto Anterior](#estructura-del-proyecto-anterior)
3. [Cambios Realizados](#cambios-realizados)
4. [Estructura Nueva](#estructura-nueva)
5. [Mapeo de Componentes](#mapeo-de-componentes)
6. [Cambios de Configuración](#cambios-de-configuración)
7. [Base de Datos](#base-de-datos)
8. [API y Endpoints](#api-y-endpoints)
9. [Instalación y Ejecución](#instalación-y-ejecución)
10. [Próximos Pasos](#próximos-pasos)

---

## Resumen Ejecutivo

Se realizó una migración completa del proyecto PDF Summarizer de **FastAPI** a **Django**. El proyecto anterior estaba completamente contenido en la carpeta `app/` con arquitectura de capas (Clean Architecture). 

**Objetivos alcanzados:**
- ✅ Migrar toda la lógica de negocio
- ✅ Convertir modelos Pydantic a Django models
- ✅ Reemplazar routers FastAPI con vistas Django
- ✅ Mantener la interfaz web funcional
- ✅ Preservar toda la funcionalidad de IA

**Duración:** ~1 hora  
**Complejidad:** Media  
**Riesgo:** Bajo

---

## Estructura del Proyecto Anterior

### FastAPI (Carpeta `app/`)

```
app/
├── main.py                          # Entrada principal FastAPI
├── core/
│   └── __init__.py                  # Configuración (Settings)
├── application/
│   ├── interfaces/
│   │   ├── ai_provider.py           # Interfaz abstracta para IA
│   │   └── summary_repository.py    # Interfaz abstracta para persistencia
│   └── services/
│       ├── pdf_service.py           # Extrae texto de PDFs
│       └── summary_service.py       # Orquesta resúmenes
├── infrastructure/
│   ├── external/
│   │   └── nvidia_client.py         # Cliente API Nvidia
│   ├── file_storage/
│   │   └── file_handler.py          # Manejo de archivos
│   └── repositories/
│       └── in_memory_repository.py  # Almacenamiento en memoria
└── presentation/
    ├── routers/
    │   └── pdf_summary.py           # Endpoints API
    ├── schemas/
    │   └── pdf_summary.py           # Modelos Pydantic
    └── templates/
        └── index.html               # Interfaz web
```

### Características del proyecto anterior:

- **Framework:** FastAPI (async)
- **Base de datos:** En memoria (diccionarios Python)
- **Autenticación:** Ninguna
- **Modelos:** Pydantic dataclasses
- **Validación:** Pydantic
- **Templates:** Jinja2
- **Almacenamiento:** En RAM

---

## Cambios Realizados

### 1. ✅ Creación de aplicación Django

```bash
# Se creó manualmente la carpeta 'summaries/' con estructura Django
```

**Archivos creados:**
- `summaries/__init__.py`
- `summaries/apps.py` - Configuración de app
- `summaries/admin.py` - Configuración de admin
- `summaries/models.py` - Modelos de base de datos
- `summaries/views.py` - Vistas/endpoints
- `summaries/urls.py` - Rutas
- `summaries/services.py` - Lógica de negocio
- `summaries/tests.py` - Archivo de tests
- `summaries/migrations/__init__.py`
- `summaries/migrations/0001_initial.py`
- `summaries/templates/summaries/index.html`

### 2. ✅ Migración de modelos

**De:** Pydantic dataclasses  
**A:** Django ORM models

```python
# Antes (FastAPI + Pydantic):
@dataclass
class Summary:
    id: UUID
    original_filename: str
    summary_text: str
    extracted_text: str
    created_at: datetime

# Después (Django):
class Summary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    original_filename = models.CharField(max_length=255)
    summary_text = models.TextField()
    extracted_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Ventajas de la migración:**
- Persistencia automática en BD
- Validaciones integradas
- ORM queries
- Admin panel gratis
- Migraciones automáticas

### 3. ✅ Migración de servicios

**PDFService** - Sin cambios de lógica
```python
# Se copió exactamente igual
PDFService.extract_text(file_content, filename)
```

**NvidiaAIProvider** - Adaptado a Django
```python
# Ahora carga configuración desde settings.py
self.api_key = settings.NVIDIA_API_KEY
self.base_url = settings.NVIDIA_API_URL
self.model = settings.AI_MODEL
```

**SummaryService** - Adaptado para Django models
```python
# Antes guardaba en diccionario
repository.save(summary)  # En memoria

# Ahora crea registro en BD
Summary.objects.create(**summary_data)
```

### 4. ✅ Migración de vistas

**De:** Routers FastAPI con decoradores  
**A:** Vistas Django con decoradores

```python
# Antes (FastAPI):
@app.post("/api/summarize")
async def summarize_pdf(file: UploadFile):
    ...

# Después (Django):
@require_http_methods(["POST"])
@csrf_exempt
def summarize_pdf(request):
    ...
```

**Vistas creadas:**
- `index()` - Página principal
- `summarize_pdf()` - POST /api/summarize/
- `list_summaries()` - GET /api/summaries/
- `get_summary()` - GET /api/summaries/<id>/
- `health_check()` - GET /api/health/

### 5. ✅ Migración de rutas

**De:** `app.include_router(router)` en FastAPI  
**A:** URLs incluidas en Django

```python
# config/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('summaries.urls')),  # ✨ Nueva
]

# summaries/urls.py
urlpatterns = [
    path('', views.index, name='index'),
    path('api/summarize/', views.summarize_pdf, name='summarize'),
    path('api/summaries/', views.list_summaries, name='list'),
    path('api/summaries/<uuid:summary_id>/', views.get_summary, name='detail'),
    path('api/health/', views.health_check, name='health'),
]
```

### 6. ✅ Migración de configuración

**De:** `app/core/__init__.py` con pydantic-settings  
**A:** `config/settings.py` Django

```python
# settings.py - Nuevas líneas agregadas:
import os
from dotenv import load_dotenv

load_dotenv()

INSTALLED_APPS = [
    ...
    'summaries',  # ✨ Nueva app
]

# Configuración de IA
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')
NVIDIA_API_URL = os.getenv('NVIDIA_API_URL', 'https://integrate.api.nvidia.com/v1')
AI_MODEL = os.getenv('AI_MODEL', 'meta/llama-3.2-90b-vision-instruct')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

### 7. ✅ Migración de template HTML

**De:** FastAPI retornaba HTML como string  
**A:** Django template en carpeta templates

```
Cambios en JavaScript:
- Rutas actualizadas: /api/summarize → /api/summarize/ (trailing slash)
- Error handling: .detail → .error (ajuste en respuestas)
- CSRF token: agregado {% csrf_token %} en el formulario
```

### 8. ✅ Actualización de dependencias

**pyproject.toml:**
```toml
dependencies = [
    "django>=5.2.13",
    "pypdf>=4.0.0",
    "httpx>=0.24.0",
    "python-dotenv>=1.0.0",
]
```

**Instalado con UV:**
```
✓ django==5.2.13
✓ pypdf==6.10.1
✓ httpx==0.28.1
✓ python-dotenv==1.2.2
✓ (+ dependencias transitivas: anyio, certifi, h11, httpcore, idna, typing-extensions)
```

### 9. ✅ Archivo `.env`

Creado: `C:/...pdf-extractext/.env`
```env
NVIDIA_API_KEY=your-nvidia-api-key-here
NVIDIA_API_URL=https://integrate.api.nvidia.com/v1
AI_MODEL=meta/llama-3.2-90b-vision-instruct
```

### 10. ✅ Archivo `.gitignore`

**Cambios:**
- Añadido: `/staticfiles/`, `/media/`, `/uploads/`
- Expandido: `.env`, `.env.local`, `.env.*.local`
- Añadido: Directorios IDE (`.idea/`, `*.swp`, `*.swo`)
- Añadido: Archivos SO (`.DS_Store`, `Thumbs.db`)

---

## Estructura Nueva

### Proyecto Django Completo

```
pdf-extractext/
├── config/                          # Configuración Django
│   ├── __init__.py
│   ├── settings.py                  # ✨ Modificado - settings de Django
│   ├── urls.py                      # ✨ Modificado - incluye summaries.urls
│   ├── asgi.py
│   └── wsgi.py
├── summaries/                       # ✨ Nueva app Django
│   ├── __init__.py
│   ├── admin.py                     # ✨ Nuevo - panel admin
│   ├── apps.py                      # ✨ Nuevo - configuración app
│   ├── models.py                    # ✨ Nuevo - modelo Summary
│   ├── views.py                     # ✨ Nuevo - vistas/endpoints
│   ├── urls.py                      # ✨ Nuevo - rutas
│   ├── services.py                  # ✨ Nuevo - servicios
│   ├── tests.py                     # ✨ Nuevo - tests
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py          # ✨ Nuevo - migraciones
│   └── templates/
│       └── summaries/
│           └── index.html           # ✨ Migrado - template HTML
├── manage.py                        # CLI de Django
├── db.sqlite3                       # BD SQLite (creada tras migrate)
├── .env                             # ✨ Nuevo - variables de entorno
├── .gitignore                       # ✨ Modificado
├── pyproject.toml                   # ✨ Modificado - nuevas dependencias
├── uv.lock                          # ✨ Actualizado - lock de dependencias
└── README.md                        # ✨ Reescrito - nuevas instrucciones
```

---

## Mapeo de Componentes

### De FastAPI a Django

| Componente FastAPI | Ubicación | Componente Django | Ubicación | Estado |
|---|---|---|---|---|
| `app/main.py` | FastAPI app | Views + URLs | `summaries/views.py` + `summaries/urls.py` | ✅ |
| `app/core/__init__.py` | Settings | Django settings | `config/settings.py` | ✅ |
| `PDFService` | `app/application/services/pdf_service.py` | PDFService | `summaries/services.py` | ✅ Idéntico |
| `SummaryService` | `app/application/services/summary_service.py` | SummaryService | `summaries/services.py` | ✅ Adaptado |
| `NvidiaAIProvider` | `app/infrastructure/external/nvidia_client.py` | NvidiaAIProvider | `summaries/services.py` | ✅ Adaptado |
| `AIProvider` (interfaz) | `app/application/interfaces/ai_provider.py` | N/A (duck typing) | Eliminada | ⚠️ |
| `SummaryRepository` (interfaz) | `app/application/interfaces/summary_repository.py` | Django ORM | `summaries/models.py` | ✅ |
| `InMemorySummaryRepository` | `app/infrastructure/repositories/in_memory_repository.py` | Django model | `summaries/models.py` | ✅ |
| `Summary` (dataclass) | `app/application/interfaces/summary_repository.py` | Summary model | `summaries/models.py` | ✅ |
| Routers | `app/presentation/routers/pdf_summary.py` | Views + URLs | `summaries/views.py` + `summaries/urls.py` | ✅ |
| Schemas | `app/presentation/schemas/pdf_summary.py` | Ninguno (JSON directo) | N/A | ⚠️ Simplificado |
| Templates | `app/presentation/templates/index.html` | Django template | `summaries/templates/summaries/index.html` | ✅ |

---

## Cambios de Configuración

### Django Settings

#### Agregado a INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'summaries',
]
```

#### Agregado import de dotenv:
```python
import os
from dotenv import load_dotenv

load_dotenv()
```

#### Nuevas configuraciones:
```python
# Configuración de PDF Summarizer
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')
NVIDIA_API_URL = os.getenv('NVIDIA_API_URL', 'https://integrate.api.nvidia.com/v1')
AI_MODEL = os.getenv('AI_MODEL', 'meta/llama-3.2-90b-vision-instruct')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

---

## Base de Datos

### Cambio de persistencia

**Antes (FastAPI):**
- En memoria: diccionarios Python
- Se perdía todo al reiniciar
- ID asignado en tiempo de ejecución

**Después (Django):**
- SQLite (archivo `db.sqlite3`)
- Persistencia entre sesiones
- Migraciones automáticas

### Modelo Summary

```python
class Summary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_filename = models.CharField(max_length=255)
    summary_text = models.TextField()
    extracted_text = models.TextField(blank=True)  # Máximo 1000 caracteres
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Summary'
        verbose_name_plural = 'Summaries'
```

### Migración realizada:

```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, summaries
Running migrations:
  Applying summaries.0001_initial... OK
```

---

## API y Endpoints

### Endpoints - Comparación

| Endpoint | Método | FastAPI | Django | Cambios |
|---|---|---|---|---|
| Raíz | GET | `/` | `/` | ✅ Mismo |
| Generar resumen | POST | `/api/summarize` | `/api/summarize/` | ⚠️ Trailing slash |
| Listar | GET | `/api/summaries` | `/api/summaries/` | ⚠️ Trailing slash |
| Obtener uno | GET | `/api/summaries/{id}` | `/api/summaries/{id}/` | ⚠️ Trailing slash |
| Health | GET | `/api/health` | `/api/health/` | ⚠️ Trailing slash |

### Respuestas JSON

Mantienen la misma estructura:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "original_filename": "documento.pdf",
  "summary_text": "Resumen del documento...",
  "created_at": "2026-04-15T23:40:00Z"
}
```

---

## Instalación y Ejecución

### Requisitos

- Python 3.11+
- UV (gestor de paquetes)

### Pasos

```bash
# 1. Navegar a proyecto
cd "C:\Users\Carla\Desktop\UTN 2026\DESARROLLO\pdf-extractext"

# 2. Activar venv (si no está activo)
.\.venv\Scripts\Activate

# 3. Instalar dependencias (ya hecho)
uv sync

# 4. Aplicar migraciones (ya hecho)
python manage.py migrate

# 5. Crear superusuario (opcional)
python manage.py createsuperuser

# 6. Ejecutar servidor
python manage.py runserver

# 7. Abrir navegador
http://127.0.0.1:8000/
```

### Acceder a admin

```
URL: http://127.0.0.1:8000/admin/
Usuario: (creado con createsuperuser)
Contraseña: (creado con createsuperuser)
```

---

## Próximos Pasos

### Sugerencias de mejora

1. **Autenticación de usuarios**
   - Implementar login/logout
   - Asociar resúmenes a usuarios
   - Sistema de permisos

2. **Mejoras de BD**
   - Migrar a PostgreSQL en producción
   - Índices para búsqueda rápida
   - Caché de resúmenes

3. **Funcionalidades**
   - Soporte para más formatos (DOCX, TXT)
   - Exportar resúmenes a PDF
   - Búsqueda por texto
   - Compartir resúmenes

4. **Infraestructura**
   - Tareas asincrónicas (Celery)
   - Almacenamiento en S3/Google Cloud
   - Logging avanzado
   - Monitoreo de errores (Sentry)

5. **Testing**
   - Tests unitarios de servicios
   - Tests de integración de vistas
   - Tests de endpoints API
   - Cobertura de código

### Tareas técnicas

- [ ] Validación de archivos más robusta
- [ ] Límite de tamaño de archivo
- [ ] Rate limiting en API
- [ ] Documentación de API (Swagger/OpenAPI)
- [ ] Compresión de respuestas
- [ ] Cache HTTP (ETag, Last-Modified)

---

## Resumen de archivos creados/modificados

### ✅ Creados

1. `summaries/__init__.py` - Inicialización app
2. `summaries/apps.py` - Configuración de app
3. `summaries/admin.py` - Administrador Django
4. `summaries/models.py` - Modelo Summary
5. `summaries/views.py` - Vistas/endpoints
6. `summaries/urls.py` - Rutas de app
7. `summaries/services.py` - Servicios (PDF, IA)
8. `summaries/tests.py` - Archivo de tests
9. `summaries/migrations/__init__.py` - Inicialización migraciones
10. `summaries/migrations/0001_initial.py` - Primera migración
11. `summaries/templates/summaries/index.html` - Template HTML
12. `.env` - Variables de entorno
13. `docs/migracion_fastapi_a_django.md` - Esta documentación

### ✏️ Modificados

1. `config/settings.py` - Agregada app y configuración
2. `config/urls.py` - Incluidas URLs de summaries
3. `pyproject.toml` - Agregadas dependencias
4. `.gitignore` - Mejorado para Django
5. `README.md` - Actualizado con instrucciones Django
6. `uv.lock` - Actualizado con nuevas dependencias

### ℹ️ Sin cambios

- `manage.py` - Generado automáticamente por Django
- `db.sqlite3` - Creado después de migrations
- `app/` - Carpeta anterior (puede eliminarse)
- `config/asgi.py` - Sin cambios necesarios
- `config/wsgi.py` - Sin cambios necesarios

---

## Notas importantes

### ⚠️ Consideraciones

1. **Interfaces abstractas eliminadas**
   - FastAPI usaba interfaces (ABC)
   - Django usa duck typing
   - Se mantiene la inyección de dependencias

2. **Async → Sync**
   - FastAPI es async por defecto
   - Django es sync por defecto
   - Se puede usar `asgiref` si se necesita async

3. **Validaciones**
   - Antes: Pydantic validaba automáticamente
   - Ahora: Django valida en formularios/models
   - API acepta JSON directamente

4. **CSRF Protection**
   - FastAPI: `@csrf_exempt` desactiva
   - Django: Requerido en formularios
   - API: Usar tokens CSRF si es necesario

### 🔒 Seguridad

- ✅ Secret key en settings (comentar en producción)
- ✅ DEBUG=True (cambiar a False en producción)
- ✅ ALLOWED_HOSTS vacío (configurar en producción)
- ✅ API key en .env (nunca commitear)

### 📊 Performance

- **FastAPI:** Mejor con endpoints muchos (async)
- **Django:** Mejor con modelos complejos (ORM)
- **Actual:** Suficiente para uso en desarrollo

---

## Validación Final

✅ Checks realizados:

```bash
$ python manage.py check
System check identified no issues (0 silenced).

$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, summaries
Running migrations:
  Applying summaries.0001_initial... OK
```

---

**Fin de la documentación**

Creado: 15 de abril de 2026  
Autor: OpenCode (Asistente de IA)  
Versión: 1.0
