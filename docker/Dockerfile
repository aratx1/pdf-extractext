FROM python:3.11-slim as builder

WORKDIR /home/app

# COPIAR DEPENDENCIAS
COPY pyproject.toml uv.lock ./

# INSTALA UV 
RUN pip install --no-cache-dir uv && \
    uv sync --no-dev

# ============= STAGE FINAL =============
FROM python:3.11-slim

# Crear usuario sin privilegios (seguridad)
RUN groupadd -r app && useradd -r -g app app

WORKDIR /home/app

# COPIAR SOLO LO NECESARIO DEL BUILDER
COPY --from=builder /home/app/.venv /home/app/.venv

# COPIA EL CODIGO
COPY app/ ./app/
COPY static/ ./static/

# DAR PERMISOS
RUN chown -R app:app /home/app

# ENTORNO VIRTUAL COMO EL PROFE 
ENV VIRTUAL_ENV=/home/app/.venv
ENV PATH="/home/app/.venv/bin:$PATH"

# CAMBIAR A USUARIO 
USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]