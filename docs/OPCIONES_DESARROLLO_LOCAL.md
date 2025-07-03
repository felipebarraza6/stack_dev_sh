# 🚀 Opciones para Desarrollo Local

## 📋 Resumen de Opciones

Tienes **3 opciones** para ejecutar el servidor de desarrollo local, dependiendo de tus necesidades:

## 🐳 Opción 1: Docker Completo (dev.yml)

### **¿Cuándo usar?**

- Cuando necesites toda la infraestructura
- Para testing completo del sistema
- Cuando trabajes con telemetría y procesamiento

### **¿Qué incluye?**

- ✅ API Django completa
- ✅ PostgreSQL (base de datos)
- ✅ Redis (cache)
- ✅ MQTT Broker (telemetría)
- ✅ Celery Worker (tareas background)
- ✅ Celery Beat (tareas programadas)
- ✅ Flower (monitoreo Celery)
- ✅ Nginx (servidor web)

### **Comando:**

```bash
cd docker/development
docker-compose -f dev.yml up --build
```

### **Endpoints:**

- API: http://localhost:8000
- Admin: http://localhost:8000/admin
- Flower: http://localhost:5555
- Nginx: http://localhost:80

---

## 🐳 Opción 2: Docker Simplificado (dev-simple.yml)

### **¿Cuándo usar?**

- Para testing de endpoints básicos
- Cuando solo necesites modelo base
- Para validar la arquitectura de dos capas

### **¿Qué incluye?**

- ✅ API Django (solo modelo base)
- ✅ SQLite (base de datos)
- ✅ Redis (cache básico)
- ❌ Sin telemetría
- ❌ Sin Celery
- ❌ Sin MQTT

### **Comando:**

```bash
# Usar el script
./scripts/run-docker-simple.sh

# O manualmente
cd docker/development
docker-compose -f dev-simple.yml up --build
```

### **Endpoints:**

- API Base: http://localhost:8000/api/base/
- API Frontend: http://localhost:8000/api/frontend/
- Admin: http://localhost:8000/admin/

---

## 💻 Opción 3: Desarrollo Local Directo

### **¿Cuándo usar?**

- Para desarrollo rápido
- Cuando no quieras usar Docker
- Para debugging directo

### **¿Qué incluye?**

- ✅ Django directo en tu máquina
- ✅ SQLite local
- ✅ Cache en memoria
- ❌ Sin telemetría
- ❌ Sin servicios externos

### **Comando:**

```bash
# Usar el script
./scripts/run-local.sh

# O manualmente
export DJANGO_SETTINGS_MODULE=api.config.settings.local
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### **Endpoints:**

- API Base: http://localhost:8000/api/base/
- API Frontend: http://localhost:8000/api/frontend/
- Admin: http://localhost:8000/admin/

---

## 🎯 Recomendación para tu Caso

### **Para Testing de Endpoints Iniciales:**

**Usa la Opción 2 (Docker Simplificado)** porque:

✅ **Ventajas:**

- Solo modelo base (sin telemetría)
- SQLite para desarrollo rápido
- Incluye Redis para cache
- Configuración automática
- Fácil de detener/iniciar

✅ **Perfecto para:**

- Validar arquitectura de dos capas
- Testing de endpoints básicos
- Verificar serializers
- Probar sistema de cache

### **Comando Recomendado:**

```bash
./scripts/run-docker-simple.sh
```

---

## 📊 Comparación de Opciones

| Característica    | Docker Completo | Docker Simple | Local Directo   |
| ----------------- | --------------- | ------------- | --------------- |
| **Velocidad**     | 🐌 Lento        | ⚡ Rápido     | ⚡⚡ Muy rápido |
| **Recursos**      | 🔥 Muchos       | ⚡ Moderados  | 💡 Mínimos      |
| **Complejidad**   | 🔥 Compleja     | ⚡ Simple     | 💡 Muy simple   |
| **Telemetría**    | ✅ Completa     | ❌ Básica     | ❌ Básica       |
| **Cache**         | ✅ Redis        | ✅ Redis      | ❌ Memoria      |
| **Base de datos** | ✅ PostgreSQL   | ✅ SQLite     | ✅ SQLite       |
| **Setup**         | 🔥 Complejo     | ⚡ Simple     | 💡 Muy simple   |

---

## 🚀 Próximos Pasos

### **1. Para Testing Inicial:**

```bash
./scripts/run-docker-simple.sh
```

### **2. Para Desarrollo Completo:**

```bash
cd docker/development
docker-compose -f dev.yml up --build
```

### **3. Para Desarrollo Rápido:**

```bash
./scripts/run-local.sh
```

**¡Elige la opción que mejor se adapte a tus necesidades!** 🎯
