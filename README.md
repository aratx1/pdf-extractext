# proyecto pdf-extractext

Extraer texto de un pdf que es proporcionado por el usuario. Después se hace un resumen gracias a un modelo de IA.

## Tecnologias:
- Python
- FastAPI
- UV
- Modelo de IA (a definir)
- Ollama (opcional, a definir a futuro)
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

### Requisitos
- Python >= 3.11
- Node.js >= 18
- npm

### Instalación

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

### Ejecutar la aplicación

```bash
python -m uvicorn app.main:app --reload
```

La aplicación estará disponible en `http://localhost:8000`

## Estructura del Proyecto

```
pdf-extractext/
├── app/                          # Código principal de la aplicación
│   ├── application/             # Lógica de negocio
│   ├── core/                    # Configuración y utilidades
│   ├── infrastructure/          # Integración externa
│   ├── presentation/            # Controladores y templates
│   └── main.py                  # Entrada de FastAPI
├── static/                      # Archivos estáticos
│   └── css/                     # Estilos generados
├── config/                      # Archivos de configuración
├── docs/                        # Documentación
├── tailwind.config.js           # Configuración de Tailwind CSS
├── postcss.config.js            # Configuración de PostCSS
├── package.json                 # Dependencias Node.js
└── pyproject.toml               # Dependencias Python
```

## Desarrollo

### Tailwind CSS

Para compilar los estilos CSS durante el desarrollo:

```bash
npm run watch:css
```

Esto generará automáticamente `static/css/output.css` cada vez que haya cambios en los templates HTML.

Para hacer una compilación única:

```bash
npm run build:css
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

Para más información, consulta la [documentación de diseño](docs/README.md).

## 📚 Documentación

- [`docs/README.md`](docs/README.md) - Guía de navegación
- [`docs/COMPONENT_REFERENCE.md`](docs/COMPONENT_REFERENCE.md) - Referencia visual de componentes

