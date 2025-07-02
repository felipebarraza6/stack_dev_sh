# Makefile para Stack VPS
.PHONY: help dev prod clean check logs migrate shell superuser test

help: ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Levantar sistema en desarrollo
	@echo "🚀 Iniciando sistema en desarrollo..."
	./scripts/run-dev.sh

prod: ## Levantar sistema en producción
	@echo "🚀 Iniciando sistema en producción..."
	docker-compose -f docker/production/production.yml up -d

clean: ## Limpiar sistema
	@echo "🧹 Limpiando sistema..."
	./scripts/cleanup.sh

check: ## Verificación rápida del sistema
	@echo "🔍 Verificando sistema..."
	./scripts/check-system.sh

logs: ## Ver logs en tiempo real
	@echo "📋 Mostrando logs..."
	docker-compose -f docker/development/dev.yml logs -f

migrate: ## Ejecutar migraciones
	@echo "🔄 Ejecutando migraciones..."
	docker-compose -f docker/development/dev.yml exec api python manage.py migrate

shell: ## Abrir shell de Django
	@echo "🐍 Abriendo shell de Django..."
	docker-compose -f docker/development/dev.yml exec api python manage.py shell

superuser: ## Crear superusuario
	@echo "👤 Creando superusuario..."
	docker-compose -f docker/development/dev.yml exec api python manage.py createsuperuser

test: ## Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	docker-compose -f docker/development/dev.yml exec api python manage.py test

status: ## Ver estado de servicios
	@echo "📊 Estado de servicios:"
	docker-compose -f docker/development/dev.yml ps

stop: ## Detener servicios
	@echo "🛑 Deteniendo servicios..."
	docker-compose -f docker/development/dev.yml down

restart: ## Reiniciar servicios
	@echo "🔄 Reiniciando servicios..."
	docker-compose -f docker/development/dev.yml restart

build: ## Reconstruir imágenes
	@echo "🔨 Reconstruyendo imágenes..."
	docker-compose -f docker/development/dev.yml build --no-cache

verify: ## Verificación completa del sistema
	@echo "🔍 Verificación completa del sistema..."
	python scripts/verificar_sistema_completo.py 