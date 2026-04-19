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
- Backdrop blur para efecto moderno
- Responsive: mayor en desktop, compacto en mobile

**Clases Tailwind**:
- `sticky top-0 z-40` - Posicionamiento
- `bg-white/80 dark:bg-slate-950/80 backdrop-blur-sm` - Efecto vidrio
- `text-2xl sm:text-3xl` - Responsive typography

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
- **Hover**: Border azul, icono azul
- **File Selected**: Muestra nombre del archivo
- **Disabled**: Botón con opacidad 50%

**Clases Tailwind**:
```
border-2 border-dashed border-slate-300 dark:border-slate-700
hover:border-blue-400 dark:hover:border-blue-500
transition-colors duration-200
```

---

### 3. Result Card (Tarjeta de Resultado)

```
┌────────────────────────────────────────────────┐
│ Summary    [Verde claro]
├────────────────────────────────────────────────┤
│                                                │
│ El resumen del PDF aparece aquí...             │
│ Puede tener múltiples líneas y párrafos.       │
│ El texto se mantiene formateado.               │
│                                                │
└────────────────────────────────────────────────┘
```

**Características**:
- Aparece con animación fade-in + slide-in (300ms)
- Header con fondo degradado
- Body con padding generoso
- Preserva espacios y líneas del texto
- Dark mode completamente soportado

**Clases Tailwind**:
```
animate-in fade-in slide-in-from-bottom-4
duration-300
bg-white dark:bg-slate-900 rounded-xl shadow-md
```

---

### 4. Error Alert (Alerta de Error)

```
┌────────────────────────────────────────────────┐
│ ⚠️  Error Message Here                          │
└────────────────────────────────────────────────┘
```

**Características**:
- Borde izquierdo rojo para indicar error
- Icono SVG a la izquierda
- Mensaje descriptivo en rojo
- Desaparece al hacer nuevo resumen

**Clases Tailwind**:
```
bg-red-50 dark:bg-red-950/20
border-l-4 border-red-500 dark:border-red-400
text-red-800 dark:text-red-200
```

---

### 5. History List (Historial de Resúmenes)

```
┌────────────────────────────────────────────────┐
│ Recent Summaries                               │
│                                                │
│ ┌──────────────────────────────────────────┐   │
│ │ 📄 document1.pdf              →          │   │
│ │ Apr 16, 2026, 3:45 PM                    │   │
│ └──────────────────────────────────────────┘   │
│ ┌──────────────────────────────────────────┐   │
│ │ 📄 document2.pdf              →          │   │
│ │ Apr 16, 2026, 2:20 PM                    │   │
│ └──────────────────────────────────────────┘   │
└────────────────────────────────────────────────┘
```

**Características**:
- Items clickeables para ver resumen
- Nombre del archivo y fecha
- Icono de flecha indicando interactividad
- Hover effect (border y shadow)
- Responsive en mobile

**Clases Tailwind**:
```
hover:border-blue-300 dark:hover:border-blue-700
hover:shadow-md dark:hover:shadow-lg
transition-all duration-200
cursor-pointer
```

---

### 6. Footer

```
┌─────────────────────────────────────────────────┐
│  © 2026 PDF Summarizer. All rights reserved.    │
└─────────────────────────────────────────────────┘
```

**Características**:
- Sticky al bottom
- Backdrop blur como header
- Texto centrado y pequeño
- Respeta dark mode

---

## 🎨 Paleta de Colores

| Uso | Light | Dark |
|-----|-------|------|
| **Primario** | `blue-600` | `blue-400` |
| **Éxito** | `emerald-600` | `emerald-400` |
| **Error** | `red-600` | `red-400` |
| **Background** | `slate-50` | `slate-950` |
| **Texto** | `slate-900` | `slate-100` |

---

## 📐 Espaciado (8px System)

| Token | Píxeles | Uso |
|-------|---------|-----|
| `p-4` | 16px | Padding interior |
| `p-6` | 24px | Padding mayor |
| `p-8` | 32px | Padding secciones |
| `gap-4` | 16px | Espaciado entre elementos |
| `my-12` | 48px | Margin entre secciones |

---

## 📱 Responsive Breakpoints

| Breakpoint | Ancho | Uso |
|-----------|-------|-----|
| `sm:` | 640px | Tablets pequeñas |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Desktops |

Ejemplo:
```
text-sm sm:text-base md:text-lg  // Aumenta tamaño en pantallas más grandes
w-full sm:w-auto                 // Full width en mobile, auto en sm+
```

---

## ✨ Animaciones

| Tipo | Duración | Uso |
|------|----------|-----|
| Fade-in | 300ms | Mostrar resultados |
| Slide | 300ms | Entrada desde abajo |
| Hover | 200ms | Estados interactivos |
| Transición color | 300ms | Cambio de dark mode |

---

## ♿ Accesibilidad

✅ Implementado:
- Contraste mínimo 4.5:1 en todos los textos
- `aria-label` en secciones principales
- Iconos SVG (no emoji)
- Focus states visibles en todos los botones
- Navegación por teclado completa
- Tamaños de toque ≥ 44×44px

---

## 🌙 Dark Mode

Todos los componentes soportan dark mode automático usando el prefix `dark:`:

```html
<div class="bg-white dark:bg-slate-900">
  <!-- Blanco en light mode, slate-900 en dark mode -->
</div>
```

El sistema detecta las preferencias del navegador automáticamente.

---

**Última actualización**: Abril 18, 2026
