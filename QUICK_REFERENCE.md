# 🚀 Quick Reference - PDF Summarizer

## ⚡ 5-Minute Setup

```bash
# 1. Install dependencies
npm install

# 2. Terminal 1: Compile CSS (watch mode)
npm run watch:css

# 3. Terminal 2: Start FastAPI server
python -m uvicorn app.main:app --reload

# 4. Open browser
# http://localhost:8000
```

---

## 📍 Archivo Principal

```
app/presentation/templates/index.html
```

Todo el contenido de la aplicación está aquí con Tailwind CSS integrado.

---

## 🎨 Paleta de Colores (Copiar-Pegar)

### Tailwind Classes

```html
<!-- Primario (Azul) -->
<div class="bg-blue-600 dark:bg-blue-400">Blue Primary</div>
<button class="bg-gradient-to-r from-blue-600 to-blue-700">Gradient Blue</button>

<!-- Éxito (Esmeralda) -->
<div class="bg-emerald-600 dark:bg-emerald-400">Emerald Success</div>
<button class="bg-gradient-to-r from-emerald-600 to-emerald-700">Gradient Green</button>

<!-- Error (Rojo) -->
<div class="bg-red-600 dark:bg-red-400">Red Error</div>

<!-- Neutral (Pizarra) -->
<div class="bg-slate-50 dark:bg-slate-950">Background</div>
<p class="text-slate-900 dark:text-slate-100">Text</p>
```

---

## 📱 Responsive Breakpoints

```html
<!-- Mobile first -->
<div class="text-sm">
  Mobile: small text
</div>

<!-- Tablet+ (640px) -->
<div class="text-sm sm:text-base">
  Scales up at tablet
</div>

<!-- Desktop+ (1024px) -->
<div class="text-sm sm:text-base lg:text-lg">
  Optimal size at desktop
</div>

<!-- Padding example -->
<div class="px-4 sm:px-6 lg:px-8">
  More padding on larger screens
</div>
```

---

## 🎬 Animaciones Rápidas

```html
<!-- Fade in + slide from bottom -->
<div class="animate-in fade-in slide-in-from-bottom-4">
  Content
</div>

<!-- Hover effects -->
<button class="hover:bg-blue-700 hover:shadow-lg hover:-translate-y-0.5 transition-all">
  Hover me
</button>

<!-- Smooth transitions -->
<div class="transition-all duration-200">
  Smooth change
</div>
```

---

## 🌗 Dark Mode

```html
<!-- Automatic dark mode -->
<div class="bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100">
  Adapts to system preference
</div>

<!-- Manual dark mode (add 'dark' class to html) -->
<!-- In DevTools: Toggle dark mode manually -->
```

---

## ♿ Accesibilidad (Must-Have)

```html
<!-- Labels -->
<label for="input">Choose PDF:</label>
<input id="input" type="file">

<!-- ARIA labels -->
<button aria-label="Close modal">×</button>

<!-- Semantic HTML -->
<header>Header content</header>
<main>Main content</main>
<footer>Footer</footer>

<!-- Color + text (not just color) -->
<div class="text-red-600">
  ✗ Error: File not found
</div>
```

---

## 🧩 Componentes Reutilizables

### Button - Primary
```html
<button class="btn-primary">Click Me</button>
```

### Button - Success
```html
<button class="btn-success" disabled>Generate</button>
```

### Card
```html
<div class="card">
  <div class="card-header">
    <h3>Title</h3>
  </div>
  <div class="card-body">
    Content here
  </div>
</div>
```

### Alert - Error
```html
<div class="alert-error">
  <p>Something went wrong</p>
</div>
```

### Badge
```html
<span class="badge-primary">Primary</span>
<span class="badge-success">Success</span>
<span class="badge-error">Error</span>
```

---

## 📐 Spacing System (8px)

| Class | Size | Pixels |
|-------|------|--------|
| p-0 | 0 | 0px |
| p-2 | 0.5rem | 8px |
| p-4 | 1rem | 16px |
| p-6 | 1.5rem | 24px |
| p-8 | 2rem | 32px |

---

## 🔍 Common Patterns

### Flexbox Layout
```html
<div class="flex items-center justify-between gap-4">
  <span>Left</span>
  <span>Right</span>
</div>
```

### Centered Container
```html
<div class="max-w-4xl mx-auto px-4">
  Content centered, responsive padding
</div>
```

### Grid Layout
```html
<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <!-- ... -->
</div>
```

### Sticky Header
```html
<header class="sticky top-0 z-40">
  Stays at top when scrolling
</header>
```

---

## 🛠️ File Locations

| What | Where |
|------|-------|
| Main UI | `app/presentation/templates/index.html` |
| CSS Input | `static/css/input.css` |
| CSS Output | `static/css/output.css` |
| Tailwind Config | `tailwind.config.js` |
| Dependencies | `package.json` |
| Docs | `docs/` |

---

## 🐛 Troubleshooting

### Styles not appearing?
```bash
npm run build:css
```

### CSS seems cached?
- Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

### Dark mode not working?
- Check system preferences
- Or manually toggle in DevTools

### Tailwind class not recognized?
- Check it's in the content paths in `tailwind.config.js`
- Re-run `npm run build:css`

---

## 📖 Documentation Links

| Need | Read |
|------|------|
| Quick start | This file (you are here) |
| Setup | `docs/TAILWIND_SETUP.md` |
| Design | `docs/TAILWIND_DESIGN.md` |
| Components | `docs/COMPONENT_REFERENCE.md` |
| Checklist | `docs/VERIFICATION_CHECKLIST.md` |
| Summary | `IMPLEMENTATION_SUMMARY.md` |

---

## ✨ Pro Tips

1. **Use Chrome DevTools** - Right-click → Inspect → Edit Tailwind classes live
2. **Mobile first** - Write mobile CSS first, then add `sm:`, `md:`, `lg:` prefixes
3. **Gradients** - Use `bg-gradient-to-r from-color to-color` for beautiful gradients
4. **Hover states** - Always test `hover:` states for buttons and links
5. **Accessibility** - Use semantic HTML: `<header>`, `<main>`, `<footer>`, `<label>`
6. **Dark mode** - Test by toggling system dark mode preference

---

## 🎯 Performance Checklist

- [ ] CSS compiled: `npm run build:css`
- [ ] No console errors
- [ ] Responsive at 375px, 768px, 1024px+
- [ ] Dark mode works
- [ ] Animations smooth (no jank)
- [ ] Touch targets ≥44px
- [ ] Contrast 4.5:1+
- [ ] Keyboard navigation works

---

## 🚢 Deploy Checklist

- [ ] Run `npm run build:css` (production build)
- [ ] Test on mobile device
- [ ] Verify dark mode
- [ ] Check accessibility (Lighthouse)
- [ ] No console errors
- [ ] All images optimized

---

**Version**: 1.0  
**Last Updated**: Abril 16, 2026  
**Status**: ✅ Ready

