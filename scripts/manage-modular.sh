#!/bin/bash

# Script para gestionar servicios modulares de telemetría
# Uso: ./manage-modular.sh [comando] [servicio]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
COMPOSE_FILE="docker-compose.modular.yml"
SERVICES=("core" "telemetry" "compliance" "all")

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}Script de Gestión de Servicios Modulares de Telemetría${NC}"
    echo ""
    echo "Uso: $0 [comando] [servicio]"
    echo ""
    echo "Comandos disponibles:"
    echo "  start     - Iniciar servicios"
    echo "  stop      - Detener servicios"
    echo "  restart   - Reiniciar servicios"
    echo "  status    - Mostrar estado de servicios"
    echo "  logs      - Mostrar logs de servicios"
    echo "  build     - Construir imágenes"
    echo "  clean     - Limpiar contenedores y volúmenes"
    echo "  migrate   - Ejecutar migraciones"
    echo "  shell     - Abrir shell en contenedor"
    echo "  health    - Verificar salud de servicios"
    echo ""
    echo "Servicios disponibles:"
    echo "  core       - Servicio principal (usuarios, catchment)"
    echo "  telemetry  - Servicio de telemetría"
    echo "  compliance - Servicio de cumplimiento"
    echo "  all        - Todos los servicios"
    echo ""
    echo "Ejemplos:"
    echo "  $0 start all"
    echo "  $0 logs telemetry"
    echo "  $0 restart core"
    echo "  $0 health all"
}

# Función para mostrar mensajes
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para verificar si Docker está ejecutándose
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker no está ejecutándose"
        exit 1
    fi
}

# Función para verificar si el archivo docker-compose existe
check_compose_file() {
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_error "Archivo $COMPOSE_FILE no encontrado"
        exit 1
    fi
}

# Función para obtener nombre del servicio
get_service_name() {
    local service=$1
    case $service in
        "core")
            echo "api-core"
            ;;
        "telemetry")
            echo "api-telemetry"
            ;;
        "compliance")
            echo "api-compliance"
            ;;
        "all")
            echo "api-core api-telemetry api-compliance"
            ;;
        *)
            log_error "Servicio '$service' no válido"
            exit 1
            ;;
    esac
}

# Función para iniciar servicios
start_services() {
    local service=$1
    log_info "Iniciando servicio(s): $service"
    
    if [ "$service" = "all" ]; then
        docker-compose -f $COMPOSE_FILE up -d
    else
        local service_name=$(get_service_name $service)
        docker-compose -f $COMPOSE_FILE up -d $service_name
    fi
    
    log_info "Servicio(s) iniciado(s) correctamente"
}

# Función para detener servicios
stop_services() {
    local service=$1
    log_info "Deteniendo servicio(s): $service"
    
    if [ "$service" = "all" ]; then
        docker-compose -f $COMPOSE_FILE down
    else
        local service_name=$(get_service_name $service)
        docker-compose -f $COMPOSE_FILE stop $service_name
    fi
    
    log_info "Servicio(s) detenido(s) correctamente"
}

# Función para reiniciar servicios
restart_services() {
    local service=$1
    log_info "Reiniciando servicio(s): $service"
    
    if [ "$service" = "all" ]; then
        docker-compose -f $COMPOSE_FILE restart
    else
        local service_name=$(get_service_name $service)
        docker-compose -f $COMPOSE_FILE restart $service_name
    fi
    
    log_info "Servicio(s) reiniciado(s) correctamente"
}

# Función para mostrar estado de servicios
show_status() {
    local service=$1
    log_info "Estado de servicio(s): $service"
    
    if [ "$service" = "all" ]; then
        docker-compose -f $COMPOSE_FILE ps
    else
        local service_name=$(get_service_name $service)
        docker-compose -f $COMPOSE_FILE ps $service_name
    fi
}

# Función para mostrar logs
show_logs() {
    local service=$1
    log_info "Mostrando logs de servicio(s): $service"
    
    if [ "$service" = "all" ]; then
        docker-compose -f $COMPOSE_FILE logs -f
    else
        local service_name=$(get_service_name $service)
        docker-compose -f $COMPOSE_FILE logs -f $service_name
    fi
}

# Función para construir imágenes
build_images() {
    local service=$1
    log_info "Construyendo imagen(es) para servicio(s): $service"
    
    if [ "$service" = "all" ]; then
        docker-compose -f $COMPOSE_FILE build
    else
        local service_name=$(get_service_name $service)
        docker-compose -f $COMPOSE_FILE build $service_name
    fi
    
    log_info "Imagen(es) construida(s) correctamente"
}

# Función para limpiar
clean_services() {
    log_warn "Limpiando contenedores y volúmenes"
    docker-compose -f $COMPOSE_FILE down -v
    docker system prune -f
    log_info "Limpieza completada"
}

# Función para ejecutar migraciones
run_migrations() {
    local service=$1
    log_info "Ejecutando migraciones para servicio(s): $service"
    
    if [ "$service" = "all" ]; then
        docker-compose -f $COMPOSE_FILE exec api-core python manage.py migrate
        docker-compose -f $COMPOSE_FILE exec api-telemetry python manage.py migrate
        docker-compose -f $COMPOSE_FILE exec api-compliance python manage.py migrate
    else
        local service_name=$(get_service_name $service)
        docker-compose -f $COMPOSE_FILE exec $service_name python manage.py migrate
    fi
    
    log_info "Migraciones completadas"
}

# Función para abrir shell
open_shell() {
    local service=$1
    log_info "Abriendo shell en servicio: $service"
    
    local service_name=$(get_service_name $service)
    docker-compose -f $COMPOSE_FILE exec $service_name /bin/bash
}

# Función para verificar salud
check_health() {
    local service=$1
    log_info "Verificando salud de servicio(s): $service"
    
    if [ "$service" = "all" ]; then
        local services=("api-core" "api-telemetry" "api-compliance")
        for s in "${services[@]}"; do
            echo -e "${BLUE}Verificando $s...${NC}"
            if docker-compose -f $COMPOSE_FILE exec $s curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
                echo -e "${GREEN}✓ $s está saludable${NC}"
            else
                echo -e "${RED}✗ $s no está respondiendo${NC}"
            fi
        done
    else
        local service_name=$(get_service_name $service)
        if docker-compose -f $COMPOSE_FILE exec $service_name curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $service_name está saludable${NC}"
        else
            echo -e "${RED}✗ $service_name no está respondiendo${NC}"
        fi
    fi
}

# Función principal
main() {
    local command=$1
    local service=${2:-"all"}
    
    # Verificar argumentos
    if [ -z "$command" ]; then
        show_help
        exit 1
    fi
    
    # Verificar Docker y archivo compose
    check_docker
    check_compose_file
    
    # Ejecutar comando
    case $command in
        "start")
            start_services $service
            ;;
        "stop")
            stop_services $service
            ;;
        "restart")
            restart_services $service
            ;;
        "status")
            show_status $service
            ;;
        "logs")
            show_logs $service
            ;;
        "build")
            build_images $service
            ;;
        "clean")
            clean_services
            ;;
        "migrate")
            run_migrations $service
            ;;
        "shell")
            if [ "$service" = "all" ]; then
                log_error "No se puede abrir shell para 'all'. Especifique un servicio específico."
                exit 1
            fi
            open_shell $service
            ;;
        "health")
            check_health $service
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "Comando '$command' no válido"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@" 