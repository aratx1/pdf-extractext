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

### Filosofía de Diseño

La aplicación utiliza un enfoque de **diseño minimalista refinado** con Tailwind CSS, enfocado en:
- **Claridad**: Interfaz limpia y fácil de usar
- **Accesibilidad**: Cumplimiento con estándares WCAG 2.1 AA
- **Responsive**: Funciona perfectamente en mobile, tablet y desktop
- **Dark Mode**: Soporte completo para modo oscuro

### Componentes UI

| Componente | Descripción | Ubicación |
|------------|-------------|-----------|
| **Header** | Encabezado sticky con título y descripción | `index.html:11-19` |
| **Upload Area** | Sección de carga de archivos PDF | `index.html:23-41` |
| **Result Card** | Mostrador del resumen generado | `index.html:44-55` |
| **Error Alert** | Alertas de error con icono | `index.html:57-68` |
| **History List** | Lista de resúmenes recientes | `index.html:70-82` |

### Paleta de Colores

- **Primario**: Azul (600-700) para acciones y acentos
- **Éxito**: Verde Esmeralda (600-700) para botones de acción positiva
- **Error**: Rojo (600-700) para mensajes de error
- **Neutral**: Pizarra (50-900) para backgrounds y texto

### Accesibilidad

✅ Cumplimiento WCAG 2.1 AA:
- Contraste de color 4.5:1+ (texto normal)
- Navegación por teclado completa
- Etiquetas ARIA apropiadas
- Iconos SVG (no emoji)
- Tamaños de toque ≥44×44px

### Características de Diseño

- **Animaciones suaves**: Transiciones de 150-300ms
- **Feedback visual**: Hover/active states en todos los elementos interactivos
- **Modo oscuro**: Automático basado en preferencias del sistema
- **Scroll suave**: Navegación fluida entre secciones
- **Gradientes**: Uso discreto para crear jerarquía visual

## 📚 Documentación

Para más detalles sobre el diseño y configuración, consulta:

- [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md) - **Resumen ejecutivo del proyecto** (COMIENZA AQUÍ)
- [`docs/README.md`](docs/README.md) - **Índice de documentación** (Guía de navegación)
- [`docs/TAILWIND_DESIGN.md`](docs/TAILWIND_DESIGN.md) - Documentación completa del diseño y componentes UI
- [`docs/TAILWIND_SETUP.md`](docs/TAILWIND_SETUP.md) - Guía de setup y mejores prácticas de Tailwind CSS
- [`docs/COMPONENT_REFERENCE.md`](docs/COMPONENT_REFERENCE.md) - Referencia visual de componentes
- [`docs/CHANGELOG.md`](docs/CHANGELOG.md) - Cambios realizados en detalle
- [`docs/VERIFICATION_CHECKLIST.md`](docs/VERIFICATION_CHECKLIST.md) - Checklist para verificación visual

### Archivos de Configuración Importantes

- `tailwind.config.js` - Configuración de Tailwind (content paths, themes)
- `postcss.config.js` - Configuración de PostCSS (Tailwind + Autoprefixer)
- `static/css/input.css` - CSS fuente con componentes personalizados
- `static/css/output.css` - CSS compilado (generado automáticamente)

## Workflow de Desarrollo

### Desarrollo Frontend

1. **Inicia el compilador CSS** en una terminal:
   ```bash
   npm run watch:css
   ```
   Esto compilará automáticamente los cambios en HTML.

2. **En otra terminal, inicia el servidor** de FastAPI:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

3. **Abre el navegador** en `http://localhost:8000`

4. **Edita los templates** en `app/presentation/templates/index.html`
   - Los cambios en CSS se reflejan automáticamente
   - Para cambios en Python, la aplicación se reinicia automáticamente

### Testing

Para verificar que el diseño funciona correctamente:

- [ ] Prueba en navegadores modernos (Chrome, Firefox, Safari, Edge)
- [ ] Verifica modo oscuro (preferencias del sistema o inspector)
- [ ] Prueba en mobile (responsive al 375px)
- [ ] Prueba navegación por teclado
- [ ] Verifica contraste de colores (WAVE, Lighthouse)

## Próximos Pasos

- [ ] Agregar más plantillas reutilizables
- [ ] Implementar toggle de tema oscuro en la interfaz
- [ ] Agregar animaciones de página más sofisticadas
- [ ] Crear componentes como snippets reutilizables
- [ ] Documentar patrones de uso común

