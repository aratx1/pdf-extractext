# Tailwind CSS Setup & Best Practices Guide

## Quick Start

### Prerequisites
- Node.js >= 18
- npm >= 8

### Installation

The Tailwind CSS setup is already configured. To get started:

1. **Install dependencies** (if not already done):
```bash
npm install
```

2. **Compile CSS** for development:
```bash
npm run watch:css
```
This command watches for changes in HTML files and automatically recompiles CSS.

3. **Verify installation**:
Check that `static/css/output.css` is generated and imported in `index.html`:
```html
<link rel="stylesheet" href="/static/css/output.css">
```

---

## Configuration Files

### `tailwind.config.js`
Tailwind configuration file that specifies:
- **Content paths**: Where to scan for Tailwind classes
- **Theme extensions**: Custom colors, fonts, spacing
- **Plugins**: Additional Tailwind extensions

Current configuration scans: `app/presentation/templates/**/*.{html,js}`

**To add new template paths**, update the `content` array:
```javascript
content: [
  "./app/presentation/templates/**/*.{html,js}",
  // Add new paths here
  "./app/other_location/**/*.{html,js}",
]
```

### `postcss.config.js`
PostCSS configuration that processes CSS through:
1. **tailwindcss**: Generates Tailwind utilities
2. **autoprefixer**: Adds vendor prefixes for browser compatibility

### `static/css/input.css`
Source CSS file with:
- Tailwind directives (`@tailwind base`, `@components`, `@utilities`)
- Custom component layers (@layer components)
- Custom animations (@layer utilities)

### `package.json` Scripts
```json
{
  "scripts": {
    "build:css": "tailwindcss -i ./static/css/input.css -o ./static/css/output.css",
    "watch:css": "tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"
  }
}
```

---

## Development Workflow

### 1. Run Watch Mode
```bash
npm run watch:css
```
Keep this running in a terminal while developing. It automatically recompiles CSS when you:
- Add/remove/modify Tailwind classes in HTML
- Change `static/css/input.css`

### 2. Edit Templates
Make changes to `app/presentation/templates/index.html` (or add new templates).

### 3. Verify Compilation
- Check browser console for errors
- Inspect computed styles in DevTools
- CSS is automatically updated

### 4. Preview Changes
- Refresh the browser to see updated styles
- For Tailwind changes without server restart: Clear browser cache if needed

---

## Using Tailwind in HTML

### Utility-First Approach

Instead of writing custom CSS, use Tailwind utility classes:

```html
<!-- ❌ Avoid: Custom CSS -->
<div style="background-color: white; padding: 1.5rem; border-radius: 0.5rem;">
  Content
</div>

<!-- ✅ Use: Tailwind utilities -->
<div class="bg-white p-6 rounded-lg">
  Content
</div>
```

### Common Patterns

#### Flexbox Layouts
```html
<div class="flex items-center justify-between gap-4">
  <span>Left</span>
  <span>Right</span>
</div>
```

#### Grid Layouts
```html
<div class="grid grid-cols-2 gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
</div>
```

#### Responsive Sizing
```html
<!-- Mobile: text-sm, sm screen+: text-base, md screen+: text-lg -->
<p class="text-sm sm:text-base md:text-lg">Responsive text</p>
```

#### Dark Mode
```html
<!-- Light mode: white background, dark mode: slate-900 -->
<div class="bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100">
  Content
</div>
```

#### Hover/Active States
```html
<button class="bg-blue-600 hover:bg-blue-700 active:scale-95 transition-all">
  Click Me
</button>
```

---

## Custom Components

Custom reusable components are defined in `static/css/input.css` using `@layer components`.

### Available Custom Classes

#### Buttons
```html
<!-- Primary button (blue) -->
<button class="btn-primary">Primary Action</button>

<!-- Success button (green) - with disabled state -->
<button class="btn-success" disabled>Success Action</button>
```

#### Cards
```html
<div class="card">
  <div class="card-header">
    <h3>Header Title</h3>
  </div>
  <div class="card-body">
    Content here
  </div>
</div>
```

#### Alerts
```html
<div class="alert-error">
  <p>Error message</p>
</div>
```

#### Badges
```html
<span class="badge-primary">Primary</span>
<span class="badge-success">Success</span>
<span class="badge-error">Error</span>
```

---

## Color System

### Palette Overview

| Role | Light | Dark |
|------|-------|------|
| **Primary** | blue-600 | blue-400 |
| **Secondary** | slate-600 | slate-400 |
| **Success** | emerald-600 | emerald-400 |
| **Error** | red-600 | red-400 |
| **Background** | slate-50 | slate-950 |
| **Surface** | white | slate-900 |

### Using Colors

```html
<!-- Background color -->
<div class="bg-blue-600 dark:bg-blue-500">Background</div>

<!-- Text color -->
<p class="text-slate-900 dark:text-slate-100">Text</p>

<!-- Border color -->
<div class="border border-slate-300 dark:border-slate-700">Border</div>

<!-- Gradient background -->
<div class="bg-gradient-to-r from-blue-600 to-blue-700">Gradient</div>
```

---

## Spacing System

Tailwind uses an 8px base unit for spacing:

| Class | Value | Pixels |
|-------|-------|--------|
| `p-0` | 0 | 0px |
| `p-1` | 0.25rem | 4px |
| `p-2` | 0.5rem | 8px |
| `p-3` | 0.75rem | 12px |
| `p-4` | 1rem | 16px |
| `p-6` | 1.5rem | 24px |
| `p-8` | 2rem | 32px |

### Examples

```html
<!-- Padding -->
<div class="p-4">Padding all sides</div>
<div class="px-4 py-2">Horizontal & vertical</div>

<!-- Margin -->
<div class="m-4">Margin all sides</div>
<div class="mb-8">Margin bottom</div>

<!-- Gap (flexbox/grid) -->
<div class="flex gap-4">Flex items with gap</div>
```

---

## Responsive Design

### Breakpoints

| Prefix | Screen Size |
|--------|------------|
| (none) | Mobile first (< 640px) |
| `sm:` | 640px and up |
| `md:` | 768px and up |
| `lg:` | 1024px and up |
| `xl:` | 1280px and up |
| `2xl:` | 1536px and up |

### Mobile-First Approach

Always start with mobile styles, then add responsive prefixes:

```html
<!-- Mobile: 1 column, sm+: 2 columns, lg+: 3 columns -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Mobile: text-sm, sm+: text-base -->
<p class="text-sm sm:text-base">Responsive text</p>
```

---

## Dark Mode

Dark mode is enabled using the `dark:` prefix.

### Implementing Dark Mode

1. **User has system preference**: Tailwind respects `prefers-color-scheme`
2. **Toggle dark mode**: Add class to `<html>` element
3. **Use dark: prefix**: Style elements for dark mode

### Example

```html
<div class="bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100">
  Light background with dark text (light mode)
  Dark background with light text (dark mode)
</div>
```

### Dark Mode in Practice

The PDF Summarizer template already supports dark mode across all components:

```html
<body class="bg-gradient-to-b from-slate-50 to-slate-100 
             dark:from-slate-950 dark:to-slate-900">
  <!-- All elements use dark: variants -->
</body>
```

---

## Animations & Transitions

### Built-in Tailwind Animations

```html
<!-- Fade in -->
<div class="animate-fade-in">Fades in</div>

<!-- Duration and timing function -->
<button class="transition-all duration-200 hover:scale-105">
  Smooth hover effect
</button>
```

### Custom Animations (in `input.css`)

```html
<!-- Slide in from bottom with fade -->
<div class="animate-in fade-in slide-in-from-bottom-4">
  Animates in
</div>

<!-- Slide in from top -->
<div class="animate-in fade-in slide-in-from-top-2">
  Error alert animates in
</div>
```

---

## Common Issues & Solutions

### Issue: Classes Not Applied
**Problem**: Tailwind classes don't appear in compiled CSS.
- **Solution**: Check that file path is in `tailwind.config.js` `content` array
- **Verify**: Run `npm run build:css` to force recompile

### Issue: Dark Mode Not Working
**Problem**: Dark mode styles don't appear.
- **Solution**: Ensure `dark:` prefix is used in classes
- **Verify**: Check if browser's dark mode setting or `<html class="dark">`

### Issue: Styles Look Pixelated/Blurry
**Problem**: Animations or scaling looks poor.
- **Solution**: Verify GPU acceleration is enabled
- **Use**: `transform`/`opacity` instead of animating width/height

### Issue: Overflow or Layout Shift
**Problem**: Content breaks layout or shifts unexpectedly.
- **Solution**: Use `max-w-*` containers, `overflow-hidden`, or `break-words`
- **Example**: `max-w-4xl`, `overflow-hidden`, `text-wrap`

---

## Best Practices

### 1. Use Semantic HTML
```html
<!-- ✅ Good: Semantic with Tailwind -->
<header class="bg-white border-b">
  <nav class="flex items-center gap-4">
    <h1 class="font-bold">Logo</h1>
  </nav>
</header>

<!-- ❌ Avoid: Non-semantic with classes -->
<div class="header">
  <div class="nav">
    <div class="title">Logo</div>
  </div>
</div>
```

### 2. Use Component Classes for Repetition
```html
<!-- ❌ Repetitive -->
<button class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
  Button 1
</button>
<button class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
  Button 2
</button>

<!-- ✅ Use component class -->
<button class="btn-primary">Button 1</button>
<button class="btn-primary">Button 2</button>
```

### 3. Responsive First
```html
<!-- ✅ Mobile-first approach -->
<div class="text-sm sm:text-base md:text-lg">
  Content
</div>

<!-- ❌ Avoid desktop-first -->
<div class="text-lg md:text-sm sm:text-xs">
  Content
</div>
```

### 4. Accessibility
```html
<!-- ✅ Include alt text, labels, aria-labels -->
<img alt="PDF Icon" src="icon.svg" />
<label for="pdf-input" class="sr-only">
  Choose PDF file
</label>

<!-- ❌ Avoid unlabeled elements -->
<img src="icon.svg" />
<input type="file" id="pdf-input" />
```

### 5. Organize Classes
```html
<!-- ✅ Organized and readable -->
<div class="
  bg-white dark:bg-slate-900
  rounded-lg border border-slate-200 dark:border-slate-800
  p-6 shadow-md
  transition-all duration-200
  hover:shadow-lg hover:border-blue-300
">
  Content
</div>
```

---

## Adding New Styles

### Approach 1: Use Existing Tailwind Classes (Preferred)
```html
<div class="flex items-center justify-center gap-4 p-4 bg-blue-50 rounded-lg">
  New component using only Tailwind utilities
</div>
```

### Approach 2: Add Custom Component Class
If a pattern repeats, add it to `static/css/input.css`:

```css
@layer components {
  .my-new-component {
    @apply flex items-center justify-center gap-4 p-4 bg-blue-50 rounded-lg;
  }
}
```

Then use:
```html
<div class="my-new-component">Content</div>
```

### Approach 3: Add Utility Class
For one-off utilities not in Tailwind:

```css
@layer utilities {
  .my-utility {
    @apply /* Tailwind classes here */;
  }
}
```

---

## Performance Tips

1. **Keep CSS small**: Only used utilities are included
2. **Avoid large files**: Split templates if needed
3. **Tree-shake unused**: Verify content paths are correct
4. **Minify output**: Use `npm run build:css` for production
5. **Load optimally**: CSS in `<head>` for critical path

---

## Resources

- [Tailwind CSS Docs](https://tailwindcss.com)
- [Tailwind Configuration](https://tailwindcss.com/docs/configuration)
- [Responsive Design](https://tailwindcss.com/docs/responsive-design)
- [Dark Mode](https://tailwindcss.com/docs/dark-mode)
- [Plugins & Extensions](https://tailwindcss.com/docs/plugins)

---

**Last Updated**: April 16, 2026
**Version**: 1.0
