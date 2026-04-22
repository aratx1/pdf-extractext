# 📚 Documentación - PDF Summarizer

## 🚀 Setup Rápido

```bash
uv sync              # Dependencias Python
npm install          # Dependencias Node.js
npm run watch:css    # Compilar CSS en desarrollo
python -m uvicorn app.main:app --reload  # Iniciar servidor
```

Accede a http://localhost:8000

---

## 🎨 Sistema de Diseño

| Elemento | Descripción |
|----------|-------------|
| **Framework** | Tailwind CSS v3 |
| **Colores** | Azul (acciones), Verde (éxito), Rojo (errores) |
| **Responsividad** | Mobile-first |
| **Dark Mode** | Automático |
| **Accesibilidad** | WCAG 2.1 AA |

---

## 📁 Estructura de Archivos

```
app/presentation/templates/index.html    # Template principal
static/css/output.css                    # CSS compilado
tailwind.config.js                       # Config Tailwind
```

---

# Componentes

### 1. Header
- Sticky positioning
- Gradient text
- Backdrop blur
- Responsive

### 2. Upload Area
- Drag & drop / click to upload
- Estados: Normal, Hover, Selected, Disabled
- Botón "Generate Summary"

### 3. Result Card
- Animación fade-in + slide-in (300ms)
- Header con fondo verde
- Preserva formato de texto
- Dark mode soportado

### 4. Error Alert
- Borde izquierdo rojo
- Icono SVG
- Auto-desaparece en nuevo resumen

### 5. History List
- Items clickeables
- Nombre archivo + fecha
- Hover effect
- Responsive

### 6. Footer
- Sticky al bottom
- Backdrop blur
- Respeta dark mode

---

## ♿ Accesibilidad

✅ Contraste 4.5:1+ | ✅ aria-labels | ✅ Navegación por teclado | ✅ Tamaños ≥44×44px

**Última actualización**: Abril 21, 2026
