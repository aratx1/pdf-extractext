# 📚 Documentación - PDF Summarizer

Bienvenido a la documentación del proyecto PDF Summarizer. Aquí encontrarás toda la información sobre el setup, diseño y componentes.

## 🚀 Inicio Rápido

### Para Desarrolladores
1. Lee [`TAILWIND_SETUP.md`](TAILWIND_SETUP.md) - Guía de instalación y configuración
2. Ejecuta `npm install` (si no está hecho)
3. Ejecuta `npm run watch:css` para compilación automática
4. Inicia el servidor: `python -m uvicorn app.main:app --reload`

### Para Diseñadores
1. Lee [`TAILWIND_DESIGN.md`](TAILWIND_DESIGN.md) - Filosofía de diseño y sistema de colores
2. Revisa [`COMPONENT_REFERENCE.md`](COMPONENT_REFERENCE.md) - Referencia visual de componentes
3. Inspecciona el código en `app/presentation/templates/index.html`

---

## 📖 Guías Disponibles

### 1. **[TAILWIND_DESIGN.md](TAILWIND_DESIGN.md)** 📐
Documentación completa del diseño visual.

**Contenido**:
- Filosofía de diseño (Minimalist-Refined)
- Sistema de colores (Light/Dark mode)
- Tipografía y escala de tipos
- Espaciado (8dp system)
- Componentes UI (Header, Upload, Result, Error, History)
- Accesibilidad (WCAG 2.1 AA)
- Implementación de Tailwind
- Testing checklist

**Mejor para**: Comprender el "por qué" detrás de cada decisión de diseño.

---

### 2. **[TAILWIND_SETUP.md](TAILWIND_SETUP.md)** ⚙️
Guía técnica de setup y mejores prácticas.

**Contenido**:
- Quick start
- Archivos de configuración
- Workflow de desarrollo
- Uso de Tailwind en HTML
- Paleta de colores
- Espaciado y responsive design
- Dark mode
- Animaciones
- Troubleshooting
- Best practices

**Mejor para**: Implementar nuevas características y mantener calidad de código.

---

### 3. **[COMPONENT_REFERENCE.md](COMPONENT_REFERENCE.md)** 🎨
Referencia visual de todos los componentes.

**Contenido**:
- Vista ASCII de cada componente
- Características y estados
- Clases Tailwind utilizadas
- Paleta de colores visual
- Tipografía y escala
- Espaciado (8dp system)
- Interacciones y animaciones
- Comportamiento responsive
- Dark mode
- Accesibilidad
- Verificación visual

**Mejor para**: Entender cómo se ven y funcionan los componentes.

---

### 4. **[CHANGELOG.md](CHANGELOG.md)** 📝
Resumen de todos los cambios realizados.

**Contenido**:
- Resumen ejecutivo
- Cambios por archivo
- Decisiones de diseño
- Componentes diseñados
- Cumplimiento de accesibilidad
- Métricas del proyecto
- Comandos disponibles
- Estructura de archivos
- Testing y verificación
- Próximos pasos

**Mejor para**: Entender qué se cambió y por qué.

---

## 🗂️ Estructura del Proyecto

```
pdf-extractext/
├── app/
│   ├── application/           # Lógica de negocio
│   ├── core/                  # Configuración
│   ├── infrastructure/        # Integraciones externas
│   ├── presentation/
│   │   ├── routers/           # Endpoints API
│   │   ├── schemas/           # Modelos de datos
│   │   └── templates/
│   │       └── index.html     # Interfaz principal (con Tailwind ✓)
│   └── main.py                # Entrada de FastAPI
├── static/
│   └── css/
│       ├── input.css          # CSS fuente (Tailwind directives + custom)
│       └── output.css         # CSS compilado ✓
├── docs/                      # 📁 Documentación
│   ├── README.md              # Este archivo
│   ├── TAILWIND_DESIGN.md
│   ├── TAILWIND_SETUP.md
│   ├── COMPONENT_REFERENCE.md
│   └── CHANGELOG.md
├── config/                    # Configuración
├── tailwind.config.js         # Configuración Tailwind ✓
├── postcss.config.js          # Configuración PostCSS ✓
├── package.json               # Dependencias npm ✓
└── README.md                  # README principal (proyecto) ✓
```

---

## 🎯 Puntos de Referencia Rápidos

### Colores
- **Primario**: `blue-600` (light) / `blue-400` (dark)
- **Éxito**: `emerald-600` (light) / `emerald-400` (dark)
- **Error**: `red-600` (light) / `red-400` (dark)
- **Background**: `slate-50` (light) / `slate-950` (dark)
- **Text**: `slate-900` (light) / `slate-100` (dark)

### Espaciado
- Basado en **8px increments** (Material Design)
- Padding: `p-4` (16px), `p-6` (24px), `p-8` (32px)
- Gaps: `gap-4` (16px)

### Responsive
- Breakpoints: `sm:` (640px), `md:` (768px), `lg:` (1024px)
- Enfoque mobile-first
- Ejemplo: `text-sm sm:text-base md:text-lg`

### Dark Mode
- Automático basado en preferencias del sistema
- Prefix: `dark:` para estilos en modo oscuro
- Ejemplo: `bg-white dark:bg-slate-900`

---

## 🛠️ Comandos Útiles

### Compilar CSS
```bash
# Development (watch mode - recompila automáticamente)
npm run watch:css

# Production (compilación única)
npm run build:css
```

### Ejecutar la aplicación
```bash
# Con reload automático
python -m uvicorn app.main:app --reload

# Sin reload
python -m uvicorn app.main:app
```

### Ver en navegador
```
http://localhost:8000
```

---

## ✅ Checklist de Verificación

Antes de hacer merge a producción:

- [ ] Estilos compilados: `npm run build:css`
- [ ] Layouts responsivos en mobile (375px), tablet (768px), desktop (1024px+)
- [ ] Dark mode funciona correctamente
- [ ] Contraste de colores cumple WCAG AA (4.5:1+)
- [ ] Navegación por teclado funciona (Tab, Enter, Escape)
- [ ] Focus indicators visibles en todos los interactivos
- [ ] Animaciones suaves (sin jank)
- [ ] No hay layout shift
- [ ] Iconos son SVG (no emoji)
- [ ] Mensajes de error claros
- [ ] Touch targets ≥44×44px
- [ ] Sin console errors

---

## 🆘 Solución de Problemas

### Problema: Las clases Tailwind no se aplican
**Solución**: Verifica que el archivo esté en la ruta de contenido de `tailwind.config.js`

### Problema: Dark mode no funciona
**Solución**: Asegúrate de usar el prefix `dark:` en las clases. Verifica las preferencias del sistema.

### Problema: CSS parece desactualizado
**Solución**: Borra el cache del navegador o ejecuta `npm run build:css` nuevamente

### Problema: Animaciones se ven pixeladas
**Solución**: Verifica que la aceleración por GPU esté habilitada. Usa `transform`/`opacity` en lugar de `width`/`height`

Ver [`TAILWIND_SETUP.md`](TAILWIND_SETUP.md) para más troubleshooting.

---

## 📚 Recursos Externos

- [Tailwind CSS Documentation](https://tailwindcss.com)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Material Design](https://material.io/design)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [MDN Web Docs](https://developer.mozilla.org)

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| Versión CSS compilado | v3 de Tailwind |
| Tamaño output.css | 27.3 KB (raw) ~3-4 KB (gzipped) |
| Componentes UI | 6 principales |
| Documentación | 4 archivos markdown |
| Cumplimiento WCAG | AA+ |
| Soporte Dark Mode | ✅ Completo |
| Responsive Breakpoints | 6 (xs-2xl) |
| Tiempo compilación | ~900ms |

---

## 🎓 Aprendizaje

### Para aprender Tailwind CSS:
1. Empieza con [`TAILWIND_SETUP.md`](TAILWIND_SETUP.md) - "Using Tailwind in HTML"
2. Inspecciona `index.html` para ver ejemplos reales
3. Experimenta modificando clases en el navegador (DevTools)
4. Consulta la [documentación oficial](https://tailwindcss.com)

### Para entender el diseño:
1. Lee [`TAILWIND_DESIGN.md`](TAILWIND_DESIGN.md) - "Design Direction"
2. Revisa [`COMPONENT_REFERENCE.md`](COMPONENT_REFERENCE.md) - "Visual Guide"
3. Prueba cambiar entre light/dark mode
4. Redimensiona el navegador para ver responsive behavior

---

## 📞 Contacto & Feedback

Para preguntas o sugerencias:
- Consulta la [documentación](.)
- Revisa el [CHANGELOG](CHANGELOG.md) para cambios recientes
- Contacta al equipo de desarrollo

---

**Última actualización**: Abril 16, 2026  
**Versión de documentación**: 1.0  
**Estado**: ✅ Completo y listo para usar

---

### Índice Rápido
- [Setup & Instalación](TAILWIND_SETUP.md#quick-start)
- [Sistema de Colores](TAILWIND_DESIGN.md#color-palette)
- [Componentes](COMPONENT_REFERENCE.md#componentes-de-la-aplicación-pdf-summarizer)
- [Accesibilidad](TAILWIND_DESIGN.md#accessibility-compliance)
- [Troubleshooting](TAILWIND_SETUP.md#common-issues--solutions)
- [Cambios Realizados](CHANGELOG.md)

