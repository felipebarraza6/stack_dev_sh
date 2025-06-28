#!/bin/bash

# Script de despliegue optimizado para SmartHydro API
set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Función para verificar requisitos
check_requirements() {
    log "Verificando requisitos..."
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        error "Docker no está instalado"
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose no está instalado"
    fi
    
    # Verificar archivo de configuración
    if [ ! -f "env.production" ]; then
        error "Archivo env.production no encontrado"
    fi
    
    log "Requisitos verificados correctamente"
}

# Función para backup de base de datos
backup_database() {
    log "Creando backup de la base de datos..."
    
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    docker-compose -f production.yml exec -T postgres pg_dump -U postgres api > "$BACKUP_DIR/database_backup.sql"
    
    if [ $? -eq 0 ]; then
        log "Backup creado en $BACKUP_DIR/database_backup.sql"
    else
        warn "No se pudo crear el backup de la base de datos"
    fi
}

# Función para detener servicios
stop_services() {
    log "Deteniendo servicios..."
    docker-compose -f production.yml down --remove-orphans
}

# Función para limpiar recursos no utilizados
cleanup_docker() {
    log "Limpiando recursos Docker no utilizados..."
    docker system prune -f
    docker volume prune -f
}

# Función para construir imágenes
build_images() {
    log "Construyendo imágenes Docker..."
    docker-compose -f production.yml build --no-cache
}

# Función para iniciar servicios
start_services() {
    log "Iniciando servicios..."
    docker-compose -f production.yml up -d
    
    # Esperar a que los servicios estén listos
    log "Esperando a que los servicios estén listos..."
    sleep 30
    
    # Verificar health checks
    check_health
}

# Función para verificar health checks
check_health() {
    log "Verificando health checks..."
    
    # Verificar PostgreSQL
    if docker-compose -f production.yml exec -T postgres pg_isready -U postgres; then
        log "PostgreSQL está saludable"
    else
        error "PostgreSQL no está respondiendo"
    fi
    
    # Verificar Django
    if curl -f http://localhost/health/ > /dev/null 2>&1; then
        log "Django está saludable"
    else
        error "Django no está respondiendo"
    fi
    
    # Verificar nginx proxy
    if curl -f http://localhost > /dev/null 2>&1; then
        log "Nginx proxy está saludable"
    else
        warn "Nginx proxy no está respondiendo"
    fi
}

# Función para ejecutar migraciones
run_migrations() {
    log "Ejecutando migraciones..."
    docker-compose -f production.yml exec -T django python manage.py migrate --noinput
}

# Función para recolectar archivos estáticos
collect_static() {
    log "Recolectando archivos estáticos..."
    docker-compose -f production.yml exec -T django python manage.py collectstatic --noinput
}

# Función para mostrar logs
show_logs() {
    log "Mostrando logs de los servicios..."
    docker-compose -f production.yml logs --tail=50
}

# Función para monitoreo
monitor_services() {
    log "Monitoreando servicios..."
    echo "Estado de los contenedores:"
    docker-compose -f production.yml ps
    
    echo ""
    echo "Uso de recursos:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
}

# Función principal
main() {
    local action=${1:-deploy}
    
    case $action in
        "deploy")
            log "Iniciando despliegue completo..."
            check_requirements
            backup_database
            stop_services
            cleanup_docker
            build_images
            start_services
            run_migrations
            collect_static
            check_health
            log "Despliegue completado exitosamente!"
            ;;
        "update")
            log "Actualizando servicios..."
            backup_database
            build_images
            docker-compose -f production.yml up -d --force-recreate
            run_migrations
            collect_static
            check_health
            log "Actualización completada!"
            ;;
        "restart")
            log "Reiniciando servicios..."
            docker-compose -f production.yml restart
            check_health
            log "Reinicio completado!"
            ;;
        "stop")
            log "Deteniendo servicios..."
            stop_services
            log "Servicios detenidos!"
            ;;
        "logs")
            show_logs
            ;;
        "monitor")
            monitor_services
            ;;
        "health")
            check_health
            ;;
        "backup")
            backup_database
            ;;
        "help"|"-h"|"--help")
            echo "Uso: $0 [comando]"
            echo ""
            echo "Comandos disponibles:"
            echo "  deploy    - Despliegue completo (por defecto)"
            echo "  update    - Actualizar servicios"
            echo "  restart   - Reiniciar servicios"
            echo "  stop      - Detener servicios"
            echo "  logs      - Mostrar logs"
            echo "  monitor   - Monitorear servicios"
            echo "  health    - Verificar health checks"
            echo "  backup    - Crear backup de base de datos"
            echo "  help      - Mostrar esta ayuda"
            ;;
        *)
            error "Comando '$action' no válido. Usa 'help' para ver comandos disponibles."
            ;;
    esac
}

# Ejecutar función principal
main "$@" 