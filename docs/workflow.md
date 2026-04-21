# Cómo aportar al proyecto

Para poder aportar y organizar al proyecto usamos una lógica de flujo de trabajo que no interfiere entre nosotros.
Creamos ramas donde cada uno trabaja a partir de develop y juntamos nuestras ramas después de revisar los cambios concretos.

## Paso a paso

1. Crea una rama a partir de develop según la nomenclatura
2. Haz tus commits a esa rama segun la nomenclatura
3. Cuando termines, haz un pull request a DEVELOP.
4. La dueña del repositorio va a hacer una review a tu código y probará tu rama
5. Cuando tus cambios están bien, tu rama hará merge con develop y tus cambios se verán en develop
6. Continua con otro issue de la misma manera

## Nomenclatura de Ramas

Usa el botón **"Create a branch"** en la página del issue. GitHub genera el nombre automáticamente:


```

<titulo-issue-como-slug>-<número-issue>

```

### Ejemplos:

```

feat-add-daily-screen-time-widget-#48
bug-login-otp-not-received-on-gmail-#2
docs-missing-schedule-api-response-example#21

```

> ⚠️ Cambia siempre la rama base a `develop` en el diálogo antes de crear — GitHub usa `main` por defecto.



## Nomenclatura de Commit

Sigue [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(alcance): descripción corta
```

| Tipo | Cuándo usarlo |
|------|--------------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `chore` | Build, dependencias, herramientas |
| `refactor` | Refactorización |
| `style` | Formato, sin cambio de lógica |
| `test` | Añadir o actualizar pruebas |
| `docs` | Documentación |
| `perf` | Mejora de rendimiento |
| `ci` | Cambios en CI/CD |

**Reglas:**
- Usa **modo imperativo** — "agregar", "corregir", "actualizar"
- Línea de asunto de menos de **72 caracteres**
- Sin punto al final
- Añade un cuerpo (línea en blanco tras el asunto) si el cambio necesita contexto

**Ejemplos:**
```
feat(auth): agregar soporte de login biométrico
```



## Pull Requests

### Formato del Título

Mismo formato `tipo(alcance): descripción` que los mensajes de commit.

### Plantilla del Cuerpo

```markdown
## Resumen

<!-- Qué hace este PR y por qué. -->

## Cambios

-
-

## Test

<!-- Pasos para verificar que los cambios funcionan. -->

## Issue(s) Relacionados

Cierra #, Cierra #
```

### Reglas

- Un tema por PR — divide los cambios no relacionados en PRs separados
- Todos los checks de CI deben pasar antes de solicitar revisión
- Resuelve todos los comentarios de revisión antes de fusionar
- Elimina la rama después de fusionar

---