# Instalación de Tailwind CSS en Django

## Descripción
Se agregó soporte para Tailwind CSS al proyecto Django utilizando el paquete `django-tailwind`.

## Cambios Realizados

### 1. Actualización de `pyproject.toml`
Se agregó `django-tailwind>=3.8.0` a la lista de dependencias del proyecto:

```toml
dependencies = [
    "django>=5.2.13",
    "pypdf>=4.0.0",
    "django-tailwind>=3.8.0",  # Nuevo
]
```

## Próximos Pasos

Para completar la instalación de Tailwind, deberás:

1. **Instalar las dependencias**:
   ```bash
   pip install -e .
   ```

2. **Agregar `tailwind` a `INSTALLED_APPS` en `settings.py`**:
   ```python
   INSTALLED_APPS = [
       # ... otras apps
       'tailwind',
   ]
   ```

3. **Inicializar el tema de Tailwind** (esto creará la carpeta `theme`):
   ```bash
   python manage.py tailwind init
   ```

4. **Configurar el compilador de Tailwind en `settings.py`**:
   ```python
   TAILWIND_APP_NAME = 'theme'  # o el nombre que hayas dado
   ```

5. **En desarrollo, ejecutar el servidor de Tailwind en paralelo**:
   ```bash
   python manage.py tailwind start
   ```

6. **En producción, compilar los estilos**:
   ```bash
   python manage.py tailwind build
   ```

## Referencias
- [django-tailwind Documentation](https://django-tailwind.readthedocs.io/)
- [Tailwind CSS](https://tailwindcss.com/)
