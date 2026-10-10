# pdf-extractext

Sube un PDF, extrae su texto y genera un resumen con un modelo de IA en la nube. Los
resúmenes se guardan en un historial, se muestran con su formato Markdown y se pueden
descargar como `.docx`.

El proyecto está dividido en **microservicios**, uno por funcionalidad, cada uno en su
propio repositorio, con **Traefik** como única puerta de entrada. Este repositorio es
la portada: la documentación general, la épica de la migración y los issues
transversales. No contiene código.

## Repositorios

| Repositorio | Qué hace | Ruta en Traefik |
|---|---|---|
| [pdf-extractext-web](https://github.com/PDF-extract-organization/pdf-extractext-web) | Interfaz y orquestador: el navegador solo habla con él | `/` y `/api` |
| [pdf-extractext-extractor](https://github.com/PDF-extract-organization/pdf-extractext-extractor) | PDF → texto (`pypdf`) | `/extractor` |
| [pdf-extractext-summarizer](https://github.com/PDF-extract-organization/pdf-extractext-summarizer) | Texto → resumen con IA (OpenRouter) | `/summarizer` |
| [pdf-extractext-summaries](https://github.com/PDF-extract-organization/pdf-extractext-summaries) | Historial de resúmenes (MongoDB) | `/summaries` |
| [pdf-extractext-exporter](https://github.com/PDF-extract-organization/pdf-extractext-exporter) | Resumen en Markdown → `.docx` | `/exporter` |
| [pdf-extractext-orchestration](https://github.com/PDF-extract-organization/pdf-extractext-orchestration) | `docker-compose` con Traefik y pruebas de extremo a extremo | — |

La arquitectura, el flujo de una petición y las decisiones de diseño están en
[`docs/estructura.md`](docs/estructura.md).

## Puesta en marcha

Todo se levanta desde el repositorio de orquestación:

```bash
git clone https://github.com/PDF-extract-organization/pdf-extractext-orchestration
cd pdf-extractext-orchestration
cp .env.example .env        # MONGO_ROOT_PASSWORD obligatoria; OPENROUTER_API_KEY para generar resúmenes
docker compose up -d --wait
```

La aplicación queda en **http://pdf.localhost** y el panel de Traefik en
http://localhost:8080. Para construir las imágenes desde el código, desarrollo
incluido, ver el README de
[pdf-extractext-orchestration](https://github.com/PDF-extract-organization/pdf-extractext-orchestration).

## Tecnologías

- **Python 3.11** con **FastAPI** y **uv** en todos los servicios
- **OpenRouter** como proveedor de IA (API compatible con la de OpenAI)
- **MongoDB** para el historial, solo accesible desde el servicio `summaries`
- **Tailwind CSS**, `marked` y `DOMPurify` en la interfaz
- **Docker**, **Docker Compose** y **Traefik v3** para el despliegue
- **GitHub Actions**: tests en cada pull request e imágenes publicadas en ghcr

## Metodologías y principios

- **TDD**: en cada servicio, un commit con los tests en rojo y otro con la
  implementación que los pone en verde
- **Arquitectura por capas con puertos**: presentación, aplicación e infraestructura;
  la capa de aplicación no importa librerías externas
- **KISS, DRY, YAGNI y SOLID**
- Los seis primeros factores de [The Twelve-Factor App](https://12factor.net/es/)
- Proyecto dirigido en GitHub con issues, ramas y pull requests: ver
  [`docs/workflow.md`](docs/workflow.md)

## El monolito anterior

Hasta octubre de 2026 la aplicación era un monolito en este mismo repositorio. Su
último estado está en la etiqueta **`monolito-v1`**:

```bash
git checkout monolito-v1
```

## Documentación

- [`docs/estructura.md`](docs/estructura.md): arquitectura, flujo de una petición y decisiones
- [`docs/workflow.md`](docs/workflow.md): ramas, commits y pull requests, comunes a los seis repositorios
