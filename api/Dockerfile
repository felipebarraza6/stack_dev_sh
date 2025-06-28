# Multi-stage build para optimizar el tamaño de la imagen
FROM python:3.11-slim as builder

# Instalar dependencias del sistema necesarias para compilar
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN groupadd -r django && useradd -r -g django django

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage de producción
FROM python:3.11-slim

# Instalar dependencias del sistema para producción
RUN apt-get update && apt-get install -y \
    postgresql-client \
    nginx \
    cron \
    gettext \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Crear usuario no-root (mismo que en builder)
RUN groupadd -r django && useradd -r -g django django

# Crear directorios necesarios
RUN mkdir -p /app /var/log/cron /var/log/nginx /var/cache/nginx

# Copiar dependencias de Python del stage anterior
COPY --from=builder /root/.local /home/django/.local

# Copiar código de la aplicación
COPY . /app/

# Configurar nginx
RUN rm -f /etc/nginx/sites-enabled/default \
    && ln -sf /app/conf/nginx-app.conf /etc/nginx/sites-enabled/ \
    && echo "daemon off;" >> /etc/nginx/nginx.conf

# Configurar permisos
RUN chown -R django:django /app /var/log/cron /var/log/nginx /var/cache/nginx \
    && chmod +x /app/docker-entrypoint.sh

# Cambiar al usuario no-root
USER django

# Configurar PATH para incluir las dependencias de Python
ENV PATH="/home/django/.local/bin:$PATH"

# Directorio de trabajo
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Exponer puerto
EXPOSE 8000

# Entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]

# Comando por defecto
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "gevent", "--worker-connections", "1000", "--max-requests", "1000", "--max-requests-jitter", "100", "--timeout", "30", "--keep-alive", "2", "api.wsgi:application"]


