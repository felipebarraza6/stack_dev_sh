#!/bin/bash
set -e

# Función para esperar a que PostgreSQL esté listo
wait_for_postgres() {
    echo "Esperando a que PostgreSQL esté listo..."
    while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
        sleep 2
    done
    echo "PostgreSQL está listo!"
}

# Función para ejecutar migraciones
run_migrations() {
    echo "Ejecutando migraciones..."
    python manage.py migrate --noinput
}

# Función para recolectar archivos estáticos
collect_static() {
    echo "Recolectando archivos estáticos..."
    python manage.py collectstatic --noinput
}

# Función para configurar cronjobs
setup_cron() {
    if [ "$1" = "cron" ]; then
        echo "Configurando cronjobs..."
        python manage.py crontab add
        python manage.py crontab show
        echo "Cronjobs configurados. Iniciando cron..."
        cron -f
    fi
}

# Función para crear superusuario si no existe
create_superuser() {
    if [ "$CREATE_SUPERUSER" = "true" ]; then
        echo "Creando superusuario..."
        python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuario creado: admin/admin123')
else:
    print('Superusuario ya existe')
"
    fi
}

# Función principal
main() {
    # Esperar a PostgreSQL
    wait_for_postgres
    
    # Ejecutar migraciones
    run_migrations
    
    # Recolectar archivos estáticos (solo en producción)
    if [ "$DJANGO_ENV" = "production" ]; then
        collect_static
    fi
    
    # Crear superusuario si es necesario
    create_superuser
    
    # Configurar cronjobs si es un contenedor de cron
    if [ "$1" = "cron" ]; then
        setup_cron "$1"
        return
    fi
    
    # Ejecutar el comando principal
    echo "Iniciando aplicación Django..."
    exec "$@"
}

# Ejecutar función principal con todos los argumentos
main "$@"
