# 📚 Documentación - PDF Summarizer

## 🚀 Setup Rápido

1. Instala dependencias:
   ```bash
   uv sync          # Python
   npm install      # Node.js (Tailwind CSS)
   ```

2. Compila CSS:
   ```bash
   npm run watch:css  # Development (watch mode)
   npm run build:css  # Production
   ```

3. Inicia el servidor:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

Accede a http://localhost:8000

---

## 📖 Documentación Disponible

### [COMPONENT_REFERENCE.md](COMPONENT_REFERENCE.md)
Referencia visual de todos los componentes UI con ejemplos de clases Tailwind.

---

## 🎨 Sistema de Diseño

| Elemento | Descripción |
|----------|-------------|
| **Framework** | Tailwind CSS v3 |
| **Colores Primarios** | Azul (acciones), Verde (éxito), Rojo (errores) |
| **Responsividad** | Mobile-first, breakpoints sm/md/lg |
| **Dark Mode** | Automático basado en preferencias del sistema |
| **Accesibilidad** | WCAG 2.1 AA (contraste 4.5:1+, navegación por teclado) |

---

## 🛠️ Comandos Útiles

```bash
# Compilar CSS (watch mode)
npm run watch:css

# Compilar CSS (una sola vez)
npm run build:css

# Iniciar servidor FastAPI
python -m uvicorn app.main:app --reload
```

---

## 📁 Estructura de Archivos Clave

```
app/presentation/templates/
└── index.html              # Template principal con Tailwind CSS

static/css/
├── input.css              # CSS fuente (Tailwind directives)
└── output.css             # CSS compilado (generado automáticamente)

tailwind.config.js         # Configuración de Tailwind
postcss.config.js          # Configuración de PostCSS
```

---

## ✅ Checklist Antes de Deploy

- [ ] `npm run build:css` completado sin errores
- [ ] Responsive en mobile (375px), tablet (768px), desktop (1024px+)
- [ ] Dark mode funciona correctamente
- [ ] Contraste de colores ≥ 4.5:1 (WCAG AA)
- [ ] Navegación por teclado funciona (Tab, Enter)
- [ ] Sin errores en consola
- [ ] Animaciones suaves

---

**Última actualización**: Abril 18, 2026
