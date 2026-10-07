

## Arquitectura implementada:

| Capa | Componentes |
|---|---|
|`Presentation` | routers/pdf_summary.py, schemas/pdf_summary.py, templates/index.html
|`Application` | services/pdf_service.py, services/summary_service.py, interfaces/ai_provider.py, interfaces/summary_repository.py
|`Infrastructure`	| external/openrouter_client.py, repositories/mongo_repository.py, repositories/in_memory_repository.py
|`Core` | core/__init__.py (Settings)

## Estructura de las carpetas

| Carpeta | Propósito |
|---|---|
| `application/interfaces` | Define qué operaciones existen (`AIProvider`, `SummaryRepository`) sin especificar cómo. Contiene también el modelo `Summary` |
| `application/services` | Coordina la lógica (subir PDF → extraer texto → enviar a IA → guardar resumen) |
| `core` | Configuración global: la clase `Settings`, que lee el `.env` |
| `infrastructure/external` | Conexión real con el proveedor de IA (OpenRouter) |
| `infrastructure/repositories` | Persistencia de resúmenes en BD |
| `presentation/routers` | Rutas HTTP (`/api/summarize`, `/api/summaries/{id}`) |
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
| `repositories/` | Persistencia de resúmenes. `MongoSummaryRepository` es la implementación en uso; `InMemorySummaryRepository` se mantiene para pruebas. |

**Principio:** Puede cambiarse completamente sin afectar capas superiores.

## Capa Core (`app/core/`)

**Responsabilidad:** Configuración global y settings.

| Componente | Propósito |
|---|---|
| `__init__.py` | Settings de la aplicación (conexión a MongoDB, API key y modelo de OpenRouter, límites). Lee variables de entorno. |

**Principio:** No contiene lógica ni modelos de dominio, solo configuración. Cualquier capa puede leerla, pero nunca escribirla.


## Visualización

```mermaid
flowchart TD
    U[Usuario sube PDF] --> R["Presentation: router<br/>valida el archivo · schemas Pydantic"]
    R --> S["Application: SummaryService<br/>extrae texto · llama al AIProvider · guarda"]
    S --> I["Infrastructure<br/>OpenRouterAIProvider · MongoSummaryRepository"]
    I --> A[Respuesta al usuario]
```

Los PDFs no se guardan: se procesan en memoria y se descartan. Lo único que se
persiste es el resumen.

## Decisiones

- **Proveedor de IA: OpenRouter.** Sustituyó a NVIDIA NIM porque se accede con una
  simple API key, sin hardware propio, y ofrece modelos gratuitos. Cambiar de
  proveedor solo exige otra implementación de `AIProvider`.
