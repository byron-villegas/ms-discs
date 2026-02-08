# Multi-stage build para reducir el tamaño de la imagen final
FROM python:3.11-slim as base

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear directorio de trabajo
WORKDIR /app

# Stage de construcción
FROM base as builder

# Instalar dependencias del sistema necesarias para compilar
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements-prod.txt .

# Instalar solo dependencias de producción
RUN pip install --user -r requirements-prod.txt

# Stage final
FROM base

# Instalar wget para healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias instaladas desde el stage builder
COPY --from=builder /root/.local /root/.local

# Asegurar que los scripts en .local están en PATH
ENV PATH=/root/.local/bin:$PATH

# Copiar código de la aplicación
COPY app/ /app/app/
COPY app.py /app/
COPY banner.txt /app/

# Crear usuario no-root para ejecutar la aplicación
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Exponer el puerto
EXPOSE 5000

# Variables de entorno por defecto
ENV FLASK_APP=app.py \
    FLASK_ENV=production

# Comando para ejecutar la aplicación con gunicorn para producción
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
