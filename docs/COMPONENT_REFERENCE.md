# Referencia Visual de Componentes

## Componentes de la Aplicación PDF Summarizer

### 1. Header (Encabezado)

```
┌─────────────────────────────────────────────────────┐
│  📄 PDF Summarizer                                  │
│     Extract and summarize your PDFs with AI         │
└─────────────────────────────────────────────────────┘
```

**Características**:
- Sticky positioning (se queda al hacer scroll)
- Gradient text en el título
- Subtitle descriptivo
- Backdrop blur para efecto moderno
- Responsive: mayor en desktop, compacto en mobile

**Clases Tailwind**:
```html
<header class="sticky top-0 z-40 border-b border-slate-200 dark:border-slate-800 
                bg-white/80 dark:bg-slate-950/80 backdrop-blur-sm">
  <h1 class="text-2xl sm:text-3xl font-bold text-gradient">PDF Summarizer</h1>
  <p class="text-sm text-slate-600 dark:text-slate-400">Extract and summarize your PDFs with AI</p>
</header>
```

---

### 2. Upload Area (Zona de Carga)

```
┌──────────────────────────────────────────────────┐
│                                                  │
│            📤  Cloud Upload Icon                 │
│                                                  │
│        [ Choose PDF File Button ]                │
│                                                  │
│        📄 example-file.pdf                       │
│                                                  │
│   [ Generate Summary Button (GREEN) ]            │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Estados**:
- **Normal**: Border dashed gris, icono gris
- **Hover**: Border azul, icono azul (indica interactividad)
- **File Selected**: Muestra nombre del archivo
- **Disabled**: Botón con opacidad 50%, no interactivo

**Clases Tailwind**:
```html
<div class="rounded-xl border-2 border-dashed border-slate-300 dark:border-slate-700 
            hover:border-blue-400 dark:hover:border-blue-500 transition-colors">
  <!-- Upload content -->
</div>
```

---

### 3. Result Card (Tarjeta de Resultado)

```
┌────────────────────────────────────────────────┐
│ Summary    [Verde claro en light, oscuro en dark]
├────────────────────────────────────────────────┤
│                                                │
│ El resumen del PDF aparece aquí...             │
│ Puede tener múltiples líneas y párrafos.       │
│ El texto se mantiene formateado.               │
│                                                │
└────────────────────────────────────────────────┘
```

**Características**:
- Aparece con animación fade-in + slide-in
- Header con fondo degradado y nombre del archivo
- Body con padding generoso
- Preserva espacios y líneas del texto
- Dark mode completamente soportado

**Animación CSS**:
```css
@keyframes slideInFromBottom {
  from {
    opacity: 0;
    transform: translateY(1rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

### 4. Error Alert (Alerta de Error)

```
┌────────────────────────────────────────────────┐
│ ❌ Failed to generate summary                  │
└────────────────────────────────────────────────┘
```

**Características**:
- Borde rojo izquierdo (border-l-4)
- Fondo rojo suave (light) o tenue (dark)
- Icono SVG rojo para claridad
- Mensaje de error cercano al icono
- Aparece con animación slide-in desde arriba

**Color Scheme**:
- Light: `bg-red-50` con `text-red-800`
- Dark: `bg-red-950/20` con `text-red-200`

---

### 5. History List (Lista de Historial)

```
┌────────────────────────────────────┐
│ Recientes Resúmenes               │
├────────────────────────────────────┤
│ 📄 documento-01.pdf          →     │
│    Hace 2 horas                    │
├────────────────────────────────────┤
│ 📄 manual-usuario.pdf        →     │
│    Hace 5 horas                    │
├────────────────────────────────────┤
│ 📄 reporte-mensual.pdf       →     │
│    Hace 1 día                      │
└────────────────────────────────────┘
```

**Características**:
- Cada item es una tarjeta clickeable
- Hover: cambio de color del border, sombra aumentada
- Icono de flecha (chevron) indicador de acción
- Nombre del archivo + fecha/hora
- Smooth transitions

**Estados de Hover**:
```css
.history-item:hover {
  border-color: rgb(147, 197, 253); /* blue-300 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 200ms ease-out;
}
```

---

## Paleta de Colores

### Light Mode

| Elemento | Color | Uso |
|----------|-------|-----|
| Primario | Blue 600-700 | Headers, links, primary CTA |
| Éxito | Emerald 600-700 | Success button, confirmación |
| Error | Red 600-700 | Alertas de error |
| Background | Slate 50-100 | Fondo de página (gradiente) |
| Text | Slate 900-700 | Texto principal |
| Subtle | Slate 400-600 | Texto secundario |

### Dark Mode

| Elemento | Color | Uso |
|----------|-------|-----|
| Primario | Blue 400-500 | Headers, links, primary CTA |
| Éxito | Emerald 400-500 | Success button, confirmación |
| Error | Red 400 | Alertas de error |
| Background | Slate 950-900 | Fondo de página (gradiente) |
| Text | Slate 100 | Texto principal |
| Subtle | Slate 300-400 | Texto secundario |

---

## Tipografía

### Escala de Tipos

| Clase | Tamaño | Peso | Uso |
|-------|--------|------|-----|
| `text-2xl/3xl` | 24-30px | Bold | Títulos principales (h1) |
| `text-xl/2xl` | 20-24px | Semibold | Subtítulos (h2) |
| `text-base` | 16px | Regular | Texto principal |
| `text-sm` | 14px | Regular | Texto secundario |
| `text-xs` | 12px | Regular | Metadata |

### Responsive Typography

- **Mobile**: `text-sm` (14px)
- **Tablet+**: `sm:text-base` (16px)
- **Desktop**: `md:text-lg` (18px)

---

## Espaciado (8dp System)

### Padding/Margin

| Clase | Valor | Uso |
|-------|-------|-----|
| `p-4` | 16px | Padding estándar |
| `p-6` | 24px | Padding generoso |
| `p-8` | 32px | Padding extra |
| `gap-4` | 16px | Espacio entre items |
| `mb-12` | 48px | Margen de sección |

### Responsive Spacing

```html
<!-- Padding: 16px mobile, 24px tablet+, 32px desktop+ -->
<div class="px-4 sm:px-6 lg:px-8">Content</div>

<!-- Margen: 24px mobile, 48px tablet+ -->
<section class="mb-6 sm:mb-12">Section</section>
```

---

## Interacciones & Animaciones

### Button States

**Default**:
```css
background: gradient-blue
```

**Hover**:
```css
background: darker-gradient-blue
box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1)
transform: translateY(-2px)
```

**Active (Click)**:
```css
transform: translateY(0)
```

**Disabled**:
```css
opacity: 0.5
cursor: not-allowed
```

### Card Hover

**Default**:
```css
border-color: slate-200 (light) / slate-800 (dark)
box-shadow: none
```

**Hover**:
```css
border-color: blue-300 (light) / blue-700 (dark)
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1)
transition: all 200ms ease-out
```

---

## Responsive Behavior

### Mobile (< 640px)

```
┌─────────────────────┐
│  📄 PDF Summarizer  │
│  Extract and...     │
└─────────────────────┘
│                     │
│  [ Upload Area ]    │
│                     │
│  [ Result Card ]    │
│                     │
│  [ History Items ]  │
│                     │
└─────────────────────┘
```

- Single column
- Smaller text (text-sm)
- Full-width buttons
- Compact padding (px-4)

### Tablet (640px - 1024px)

```
┌────────────────────────────────────┐
│  📄 PDF Summarizer                 │
│  Extract and summarize your PDFs   │
└────────────────────────────────────┘
│                                    │
│       [ Upload Area ]              │
│                                    │
│       [ Result Card ]              │
│                                    │
│    [ History List Grid ]           │
│    [Item 1] [Item 2]               │
│                                    │
└────────────────────────────────────┘
```

- Larger text (text-base)
- Increased padding (px-6)
- Better spacing

### Desktop (1024px+)

```
┌──────────────────────────────────────────┐
│  📄 PDF Summarizer                       │
│  Extract and summarize your PDFs with AI │
└──────────────────────────────────────────┘
│                                          │
│      [ Upload Area - Centered ]          │
│                                          │
│      [ Result Card - Max Width ]         │
│                                          │
│    [ History Items in Grid ]             │
│    [Item 1] [Item 2] [Item 3]            │
│                                          │
└──────────────────────────────────────────┘
```

- Optimal text size (text-lg)
- Max-width container (max-w-4xl)
- Generous padding (px-8)
- Horizontal grid for history items

---

## Dark Mode

El dark mode se activa automáticamente basado en las preferencias del sistema.

### Transición Automática

```css
body {
  transition: colors 300ms;
  /* Cambio suave entre temas */
}
```

### Ejemplo de Componente

```html
<!-- Light mode: white background with dark text -->
<!-- Dark mode: slate-900 background with light text -->
<div class="bg-white dark:bg-slate-900 
            text-slate-900 dark:text-slate-100">
  Content that adapts to theme
</div>
```

---

## Accesibilidad

### Características Incluidas

✅ **Contraste (WCAG AA)**
- Normal text: 4.5:1 ratio
- Large text: 3:1 ratio
- Validado en light y dark mode

✅ **Navegación por Teclado**
- Tab order correcto
- Enter/Space para botones
- Focus rings visibles

✅ **Iconografía**
- SVG icons (no emoji)
- Tamaños consistentes
- Contraste suficiente

✅ **Touch Targets**
- Mínimo 44×44px
- Espacio entre elementos (8px+)
- No requiere precisión exacta

✅ **Semantic HTML**
- Headings jerarquía correcta (h1 → h2)
- Form labels asociadas
- ARIA labels donde es necesario

---

## Verificación Visual

Para verificar que todo está correctamente implementado:

```html
<!-- Verifica que los gradientes se renderizan -->
<div class="bg-gradient-to-r from-blue-600 to-blue-700">
  Gradient rendered
</div>

<!-- Verifica que dark mode funciona -->
<div class="dark:bg-slate-900">
  Toggle system dark mode
</div>

<!-- Verifica animaciones -->
<div class="animate-in fade-in slide-in-from-bottom-4">
  Animation visible on page load
</div>

<!-- Verifica responsividad -->
<div class="text-sm sm:text-base md:text-lg">
  Resize browser - text changes at breakpoints
</div>
```

---

**Última Actualización**: Abril 16, 2026
**Versión**: 1.0
