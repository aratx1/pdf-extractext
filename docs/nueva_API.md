# Cambios de la API: De NVIDIA a OPENCODE

Este documento describe la transición de la API anterior basada en NVIDIA a la nueva API basada en OPENCODE (OpenRouter). El sistema ahora utiliza un modelo de IA disponible públicamente a través de OpenRouter, facilitando la integración y el acceso a modelos avanzados de lenguaje.

## Resumen de Cambios

- **Proveedor de IA:**
  - Antes: API de NVIDIA (privada o limitada).
  - Ahora: API de OPENCODE (OpenRouter), que permite el uso de modelos de IA accesibles públicamente.

- **Cliente HTTP:**
  - Se implementó un cliente en `app/infrastructure/external/openrouter_client.py` para interactuar con la API de OpenRouter.
  - El modelo y la clave de API se configuran en los settings globales (`app/core/__init__.py`).

- **Modelo de IA:**
  - El modelo utilizado es configurable y corresponde a uno de los modelos disponibles en OpenRouter (por defecto: `openrouter/free`).
  - El sistema puede adaptarse fácilmente a otros modelos soportados por OpenRouter.

- **Interfaz de proveedor de IA:**
  - Se mantiene una interfaz abstracta (`AIProvider`) para facilitar el cambio de proveedor en el futuro.

- **Uso de IA disponible:**
  - El modelo de IA utilizado es accesible públicamente y no requiere hardware especializado (como GPU NVIDIA local), solo una clave de API válida.

## Ventajas de la nueva API

- **Acceso a modelos de última generación** sin depender de infraestructura propia.
- **Escalabilidad y mantenimiento** simplificados.
- **Facilidad de integración** con otros servicios o modelos de IA.

## Ejemplo de flujo

1. El usuario sube un PDF.
2. El texto se extrae y se envía a la API de OpenRouter.
3. El modelo de IA genera un resumen y lo devuelve a la aplicación.
4. El resumen se almacena y se muestra al usuario.

## Configuración

- La clave y el modelo de OpenRouter se definen en variables de entorno o en el archivo de configuración.
- El endpoint por defecto es `https://openrouter.ai/api/v1`.

### Uso por otros desarrolladores

Si otros miembros del equipo desean utilizar la aplicación, cada uno debe:

1. Crear una cuenta en [OpenRouter](https://openrouter.ai/) y generar su propia API key.
2. Añadir la clave obtenida al archivo `.env` en la raíz del proyecto, por ejemplo:

  ```env
  OPENROUTER_API_KEY=tu_clave_aqui
  ```


Sin una clave válida, la aplicación no podrá generar resúmenes usando la IA.

## Notas

- El sistema está preparado para cambiar de proveedor de IA fácilmente gracias a la arquitectura basada en interfaces.
- El uso de IA disponible permite democratizar el acceso a la tecnología sin requerir recursos locales avanzados.
