

## Arquitectura implementada:

| Capa | Componentes |
|---|---|
|`Presentation` | routers/pdf_summary.py, schemas/pdf_summary.py, templates/index.html
|`Application` | services/pdf_service.py, services/summary_service.py, interfaces/ai_provider.py
|`Infrastructure`	| external/openrouter_client.py, repositories/in_memory_repository.py, file_storage/file_handler.py
|`Core` | core/__init__.py (Settings)

## Estructura de las carpetas

| Carpeta | Propósito |
|---|---|
| `application/interfaces` | Define qué operaciones existen (ej: `PDFRepository`) sin especificar cómo |
| `application/services` | Coordina la lógica (subir PDF → extraer texto → enviar a IA → guardar resumen) |
| `core` | Modelos base como `PDFDocument`, `Summary` |
| `infrastructure/external` | Conexión real a OpenAI u otro proveedor de IA |
| `infrastructure/file_storage` | Guardar PDFs en disco o cloud storage |
| `infrastructure/repository` | Persistencia de resúmenes en BD |
| `presentation/routers` | Rutas HTTP (`/upload`, `/summary/{id}`) |
| `presentation/schemas` | Validación de datos de entrada/salida |
| `presentation/templates` | HTML del frontend |


## Capa de Presentación (`app/presentation/`)

**Responsabilidad:** Interfaz con el cliente (usuario o sistema externo).

| Componente | Propósito |
|---|---|
| `routers/` | Define endpoints HTTP (GET, POST). Recibe requests y devuelve respuestas. |
| `schemas/` | Validación de datos de entrada/salida con Pydantic. |
| `templates/` | Plantillas HTML para la interfaz web. |

**Principio:** Solo maneja transporte, nunca lógica de negocio.

## Capa de Aplicación (`app/application/`)

**Responsabilidad:** Reglas de negocio y casos de uso.

| Componente | Propósito |
|---|---|
| `services/` | Lógica de negocio. Ej: `SummaryService` orquestra extracción + IA + persistencia. |
| `interfaces/` | Contratos (abstractos) que definen qué debe hacer cualquier implementación. |

**Principio:** No sabe cómo se persisten datos ni cómo se llama a la IA. Solo conoce las interfaces.

## Capa de Infraestructura (`app/infrastructure/`)

**Responsabilidad:** Implementaciones concretas de las interfaces.

| Componente | Propósito |
|---|---|
| `external/` | Cliente HTTP para OpenRouter API. |
| `repositories/` | Persistencia de resúmenes (in-memory, listo para SQL/NoSQL). |
| `file_storage/` | Manejo de archivos subidos (guardar, leer, eliminar). |

**Principio:** Puede cambiarse completamente sin afectar capas superiores.

## Capa Core (`app/core/`)

**Responsabilidad:** Configuración global y settings.

| Componente | Propósito |
|---|---|
| `__init__.py` | Settings de la aplicación (API keys, rutas, límites). Lee variables de entorno. |

**Principio:** Puede cambiarse completamente sin afectar capas superiores.


## Visualización

![alt text](image.png)