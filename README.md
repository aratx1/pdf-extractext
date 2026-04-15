# PDF Summarizer - Django

Aplicación Django para extraer texto de PDFs y generar resúmenes automáticos basados en análisis de frecuencia de palabras.

## Características

- ✅ Upload de archivos PDF
- ✅ Extracción de texto de PDFs
- ✅ Generación automática de resúmenes
- ✅ Historial de resúmenes
- ✅ API REST JSON
- ✅ Interfaz web moderna
- ✅ Sin dependencias externas de IA

## Tecnologías

- **Django 5.2** - Framework web
- **Python 3.11+** - Lenguaje
- **pypdf** - Lectura de PDFs
- **SQLite** - Base de datos

## Instalación

### 1. Clonar el repositorio
```bash
git clone <repo-url>
cd pdf-extractext
```

### 2. Instalar dependencias con UV
```bash
uv sync
```

O si usas pip:
```bash
pip install -r requirements.txt
```

### 3. Ejecutar migraciones
```bash
uv run python manage.py migrate
```

### 4. Iniciar servidor
```bash
uv run python manage.py runserver 
```

Visita: http://127.0.0.1:8000/

## Uso

### Interfaz Web
1. Ve a http://127.0.0.1:8000/
2. Selecciona un archivo PDF
3. Haz clic en "Generate Summary"
4. El resumen se mostrará en pantalla


## Estructura del Proyecto

```
pdf-extractext/
├── config/                 # Configuración Django
│   ├── settings.py        # Configuración principal
│   ├── urls.py            # Rutas del proyecto
│   └── wsgi.py            # WSGI app
├── summaries/             # Aplicación principal
│   ├── models.py          # Modelo Summary
│   ├── views.py           # Vistas/endpoints
│   ├── urls.py            # URLs de la app
│   ├── services.py        # Servicios (PDF, IA)
│   ├── admin.py           # Admin de Django
│   ├── migrations/        # Migraciones DB
│   └── templates/summaries/
│       └── index.html     # Interfaz web
├── manage.py              # CLI de Django
├── .env                   # Variables de entorno
└── db.sqlite3             # Base de datos

```

## Panel Administrativo

Accede al panel de administrador en:
```
http://127.0.0.1:8000/admin/
```

**Usuario/Contraseña por defecto:**
```bash
python manage.py createsuperuser
```

## Licencia

Ver archivo LICENSE

## Contacto

Para problemas o sugerencias, abre un issue en GitHub.