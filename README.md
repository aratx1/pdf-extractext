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

Antes de levantar la aplicación, edita el archivo `.env` en la raíz del proyecto y configura tu API key de OpenRouter:

```
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
```

- Genera tu API key gratis en [openrouter.ai/keys](https://openrouter.ai/keys) (solo email, sin tarjeta).
- `OPENROUTER_MODEL` debe ser un identificador válido de OpenRouter. Los modelos con sufijo `:free` no tienen costo (sí tienen rate limits).

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
├── tests/                        # Pruebas
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

- Los archivos CSS compilados se generan en `static/css/output.css`
- Asegúrate de incluir el archivo CSS compilado en tus templates HTML
- El archivo `tailwind.config.js` está configurado para buscar clases de Tailwind en `app/presentation/templates/`

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

