# proyecto pdf-extractext

Extraer texto de un pdf que es proporcionado por el usuario. Después se hace un resumen gracias a un modelo de IA.

## Tecnologias:
- Python
- FastAPI
- UV
- OpenRouter (proveedor de IA en la nube)
- Tailwind CSS (para estilos)
- Base de datos no relacional MongoDB

## Metodologías: 

- TDD
- Proyecto digirido en Github
- Los seis primeros principios de 12 factor APP

## Principios de programación:

- KISS
- DRY
- YAGNI
- SOLID

## Setup

### Configuración del entorno

El repositorio no incluye el `.env` (está en `.gitignore`). Antes de levantar la
aplicación, crea el tuyo copiando la plantilla:

```bash
cp .env.example .env
```

En Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

Después edita `.env` y configura como mínimo tu API key de OpenRouter:

```
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=openrouter/free
```

- Genera tu API key gratis en [openrouter.ai/keys](https://openrouter.ai/keys) (solo email, sin tarjeta).
- `OPENROUTER_MODEL` debe ser un identificador válido del [catálogo de OpenRouter](https://openrouter.ai/models). El valor por defecto, `openrouter/free`, es un router que elige automáticamente un modelo gratuito; los ids con sufijo `:free` tampoco tienen costo (sí tienen rate limits).
- El resto de variables (`MONGODB_URL`, `UPLOAD_DIR`, etc.) están descritas en `.env.example` y tienen valores por defecto válidos para desarrollo local.

Sin la API key configurada, la app responderá con un mensaje claro pidiéndola al subir el primer PDF.

### Opción A: Docker (recomendado)

Requisitos:
- Docker
- Docker Compose

Pasos:

1. **Crear la red externa que usa docker-compose:**
```bash
docker network create red_pdfextract
```

2. **Levantar el stack (app + MongoDB):**
```bash
docker compose up -d --build
```

La aplicación estará disponible en `http://localhost:8000`.

Para detenerla:
```bash
docker compose down
```

### Opción B: Ejecución local

Requisitos:
- Python >= 3.11
- Node.js >= 18 y npm
- MongoDB >= 7 corriendo en `localhost:27017` (o ajusta `MONGODB_URL` en `.env`)

Pasos:

1. **Instalar dependencias Python:**
```bash
uv sync
```

2. **Instalar dependencias Node.js (para Tailwind CSS):**
```bash
npm install
```

3. **Compilar Tailwind CSS:**
```bash
npm run build:css
```

O para desarrollo en tiempo real:
```bash
npm run watch:css
```

4. **Ejecutar la aplicación:**
```bash
python -m uvicorn app.main:app --reload
```

La aplicación estará disponible en `http://localhost:8000`.

## Tests

Instala las dependencias de desarrollo y ejecuta la suite:

```bash
uv sync --group dev
uv run pytest
```

Los tests unitarios no necesitan red, ni MongoDB, ni API key: el proveedor de IA
y el repositorio se sustituyen por dobles de prueba, y las peticiones HTTP usan
un transporte simulado.

| Archivo | Qué cubre |
|---|---|
| `tests/test_pdf_service.py` | Extracción de texto, recuento de páginas y caracteres, PDFs sin texto y archivos inválidos |
| `tests/test_summary_service.py` | Orquestación PDF → IA → persistencia, incluido el truncado del texto |
| `tests/test_in_memory_repository.py` | Guardado, búsqueda por id, orden por fecha y límite |
| `tests/test_openrouter_client.py` | Construcción de la petición y manejo de errores del proveedor de IA |
| `tests/test_api_routes.py` | Los endpoints HTTP: casos correctos, validaciones y códigos de error |

### Tests de integración

Los que dependen de servicios externos están marcados como `integration` y
quedan **excluidos de la ejecución por defecto**. Para lanzarlos:

```bash
uv run pytest -m integration
```

| Archivo | Requisito |
|---|---|
| `tests/test_mongo_repository.py` | Un MongoDB en marcha (`docker compose up -d mongodb`). Usa la base `pdf_extractext_test`, que borra al empezar y al terminar |
| `tests/test_openrouter_api.py` | `OPENROUTER_API_KEY` válida. Hace peticiones reales y consume cuota |

Si el servicio que necesitan no está disponible, se saltan solos en vez de fallar.

## API

Todos los endpoints cuelgan del prefijo `/api`. Con la aplicación levantada tienes
documentación interactiva generada por FastAPI en `http://localhost:8000/docs`.

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/summarize` | Sube un PDF (multipart, campo `file`) y devuelve el resumen generado |
| `GET` | `/api/summaries` | Lista los resúmenes guardados. Acepta `?limit=` (por defecto 100) |
| `GET` | `/api/summaries/{id}` | Devuelve un resumen concreto por su UUID |
| `GET` | `/api/summaries/{id}/export` | Descarga el resumen como archivo `.docx` |
| `GET` | `/api/health` | Estado del servicio y disponibilidad del proveedor de IA |

Además, `GET /` sirve la interfaz web y `/static` expone los archivos estáticos.

### Ejemplo

```bash
curl -X POST http://localhost:8000/api/summarize \
  -F "file=@documento.pdf"
```

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "original_filename": "documento.pdf",
  "summary_text": "El documento describe...",
  "created_at": "2026-01-15T10:30:00"
}
```

### Códigos de error

| Código | Cuándo |
|---|---|
| `400` | El archivo no es `.pdf` o está vacío |
| `404` | No existe un resumen con ese UUID |
| `502` | Falta la API key de OpenRouter o el proveedor rechazó la petición |
| `503` | No se pudo contactar con el proveedor de IA |
| `504` | El modelo tardó demasiado en responder |

### Límites

- Solo se envían al modelo los primeros 12.000 caracteres del PDF
  (`MAX_PROMPT_CHARS` en `app/application/services/summary_service.py`).
- El resumen se pide con un máximo de 500 palabras.

## Estructura del Proyecto

```
pdf-extractext/
├── app/                          # Código principal de la aplicación
│   ├── application/              # Lógica de negocio
│   │   ├── interfaces/           # Contratos (AIProvider, SummaryRepository)
│   │   └── services/             # pdf_service.py, summary_service.py
│   ├── core/                     # Settings: configuración leída del .env
│   ├── infrastructure/           # Integración externa
│   │   ├── external/             # openrouter_client.py
│   │   ├── file_storage/         # file_handler.py
│   │   └── repositories/         # mongo_repository.py, in_memory_repository.py
│   ├── presentation/             # Capa HTTP
│   │   ├── routers/              # pdf_summary.py (endpoints bajo /api)
│   │   ├── schemas/              # Modelos Pydantic de entrada/salida
│   │   └── templates/            # index.html
│   └── main.py                   # Entrada de FastAPI
├── static/                       # Archivos estáticos servidos en /static
│   ├── css/                      # input.css y output.css (generado)
│   └── media/                    # Imágenes e iconos
├── tests/                        # Pruebas (conftest.py + tests por módulo)
├── docs/                         # Documentación
├── uploads/                      # PDFs subidos (se crea al arrancar, no versionado)
├── docker-compose.yml            # Stack de Docker (app + MongoDB)
├── Dockerfile                    # Imagen de la aplicación
├── .env.example                  # Plantilla de variables de entorno
├── .env                          # Variables de entorno reales (no se comitea)
├── tailwind.config.js            # Configuración de Tailwind CSS
├── postcss.config.js             # Configuración de PostCSS
├── package.json                  # Dependencias Node.js
├── pyproject.toml                # Dependencias Python
├── uv.lock                       # Versiones bloqueadas por UV
├── main.py                       # Script inicial de `uv init` (sin uso)
└── LICENSE
```

## Notas

- Tailwind compila `static/css/input.css` en `static/css/output.css`, que
  `index.html` ya enlaza como `/static/css/output.css`.
- `tailwind.config.js` busca las clases de Tailwind en
  `app/presentation/templates/`, así que si añades plantillas fuera de esa
  carpeta tendrás que incluirlas en `content` o sus estilos no se generarán.
- Tras cambiar clases en las plantillas hay que recompilar con
  `npm run build:css` (o dejar `npm run watch:css` corriendo en desarrollo).

## Diseño & UI

La aplicación utiliza **Tailwind CSS** para un diseño minimalista refinado con:
- **Responsive**: Mobile-first, funciona en todos los tamaños
- **Dark Mode**: Automático basado en preferencias del sistema
- **Accesible**: WCAG 2.1 AA (contraste 4.5:1+, navegación por teclado)
- **Animaciones**: Transiciones suaves de 150-300ms

Para más información, consulta la [documentación de componentes](docs/COMPONENT_REFERENCE.md).

## 📚 Documentación

- [`docs/estructura.md`](docs/estructura.md) - Navegación y estructura del funcionamiento
- [`docs/nueva_API.md`](docs/nueva_API.md) - Detalle de la API
- [`docs/workflow.md`](docs/workflow.md) - Flujo de trabajo del proyecto
- [`docs/COMPONENT_REFERENCE.md`](docs/COMPONENT_REFERENCE.md) - Referencia de componentes UI

