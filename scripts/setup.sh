#!/bin/bash

# Script de configuración para SmartHydro API
# Este script ayuda a configurar el proyecto para desarrollo o producción

set -e

echo "🚀 Configurando SmartHydro API..."

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [development|production]"
    echo ""
    echo "Opciones:"
    echo "  development   Configurar para desarrollo"
    echo "  production    Configurar para producción"
    echo "  help          Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 development"
    echo "  $0 production"
}

# Función para configurar desarrollo
setup_development() {
    echo "🔧 Configurando para desarrollo..."
    
    # Copiar archivo de variables de entorno
    if [ ! -f .env ]; then
        cp env.development .env
        echo "✅ Archivo .env creado desde env.development"
    else
        echo "⚠️  El archivo .env ya existe, no se sobrescribió"
    fi
    
    # Crear directorio de logs
    mkdir -p logs
    echo "✅ Directorio de logs creado"
    
    # Crear directorio de media si no existe
    mkdir -p media
    echo "✅ Directorio de media creado"
    
    echo "🎉 Configuración de desarrollo completada!"
    echo ""
    echo "Para ejecutar el proyecto:"
    echo "  docker-compose -f local.yml up --build"
}

# Función para configurar producción
setup_production() {
    echo "🔧 Configurando para producción..."
    
    # Verificar que el archivo env.production existe
    if [ ! -f env.production ]; then
        echo "❌ Error: El archivo env.production no existe"
        exit 1
    fi
    
    # Copiar archivo de variables de entorno
    if [ ! -f .env ]; then
        cp env.production .env
        echo "✅ Archivo .env creado desde env.production"
        echo "⚠️  IMPORTANTE: Edita el archivo .env con valores seguros para producción"
    else
        echo "⚠️  El archivo .env ya existe, no se sobrescribió"
    fi
    
    # Crear directorio de logs
    mkdir -p logs
    echo "✅ Directorio de logs creado"
    
    # Crear directorio de media si no existe
    mkdir -p media
    echo "✅ Directorio de media creado"
    
    echo "🎉 Configuración de producción completada!"
    echo ""
    echo "IMPORTANTE: Antes de ejecutar en producción:"
    echo "  1. Edita el archivo .env con valores seguros"
    echo "  2. Cambia la SECRET_KEY por una clave segura"
    echo "  3. Configura las credenciales de base de datos"
    echo "  4. Configura las credenciales de email"
    echo ""
    echo "Para ejecutar el proyecto:"
    echo "  docker-compose -f production.yml up --build -d"
}

# Verificar argumentos
if [ $# -eq 0 ]; then
    echo "❌ Error: Debes especificar el entorno"
    show_help
    exit 1
fi

case $1 in
    "development"|"dev")
        setup_development
        ;;
    "production"|"prod")
        setup_production
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "❌ Error: Entorno '$1' no válido"
        show_help
        exit 1
        ;;
esac 