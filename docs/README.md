# 🚀 Stack VPS - Sistema de Telemetría y Cumplimiento

Sistema modular y profesional para la gestión de telemetría de puntos de captación con capacidades avanzadas de cumplimiento regulatorio.

## 🏗️ Arquitectura

```
stack_vps/
├── api/                    # Aplicación Django principal
│   ├── core/              # Funcionalidades centrales
│   ├── users/             # Gestión de usuarios
│   ├── providers/         # Proveedores de datos
│   ├── variables/         # Procesamiento de variables
│   ├── catchment/         # Puntos de captación
│   ├── compliance/        # Cumplimiento regulatorio
│   ├── telemetry/         # Procesamiento de telemetría
│   └── tasks/             # Tareas Celery
├── docker/                # Configuraciones Docker
│   ├── development/       # Configuración desarrollo
│   └── production/        # Configuración producción
├── scripts/               # Scripts de utilidad
├── docs/                  # Documentación
└── monitoring/            # Configuración de monitoreo
```

## 🚀 Inicio Rápido

### Desarrollo Local

```bash
# 1. Verificar sistema
python scripts/verificar_sistema_completo.py

# 2. Levantar servicios
./scripts/run-dev.sh
```

### URLs Disponibles

- **API**: http://localhost:8000
- **Nginx**: http://localhost:80
- **Flower**: http://localhost:5555

## 📚 Documentación

- [Documentación Completa](docs/README_SISTEMA_COMPLETO.md)
- [Arquitectura del Sistema](docs/architecture/)
- [API Reference](docs/api/)

## 🛠️ Comandos Útiles

```bash
# Ver todos los comandos disponibles
make help

# Desarrollo
make dev          # Levantar sistema en desarrollo
make logs         # Ver logs en tiempo real
make status       # Ver estado de servicios
make stop         # Detener servicios
make restart      # Reiniciar servicios

# Base de datos
make migrate      # Ejecutar migraciones
make shell        # Abrir shell de Django
make superuser    # Crear superusuario

# Mantenimiento
make clean        # Limpiar sistema
make build        # Reconstruir imágenes
make check        # Verificación rápida
make verify       # Verificación completa
```

## 📞 Soporte

Para soporte técnico, revisa la [documentación completa](docs/README_SISTEMA_COMPLETO.md) o ejecuta el script de verificación.
