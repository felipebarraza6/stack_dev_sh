"""
SmartHydro Alert Service - FastAPI
Microservicio para manejo de alertas basadas en condiciones y variables
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import uvicorn
import pytz
import httpx
import json
import re

from .alert_manager import AlertManager
from .models import AlertRule, AlertCondition, AlertAction, AlertExecution, VariableData
from .auth import get_current_user

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de zona horaria
CHILE_TZ = pytz.timezone('America/Santiago')

# Crear aplicación FastAPI
app = FastAPI(
    title="SmartHydro Alert Service",
    description="Microservicio para alertas basadas en condiciones y variables",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del manager de alertas
alert_manager: Optional[AlertManager] = None

# Configuración de servicios
DJANGO_API_URL = "http://business-api:8004"
NOTIFICATION_SERVICE_URL = "http://notification-service:8006"
TELEMETRY_SERVICE_URL = "http://telemetry-collector:8001"


@app.on_event("startup")
async def startup_event():
    """Inicializar el manager de alertas al arrancar"""
    global alert_manager
    
    try:
        alert_manager = AlertManager(
            database_url="postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business",
            redis_url="redis://redis:6379",
            django_api_url=DJANGO_API_URL,
            notification_service_url=NOTIFICATION_SERVICE_URL,
            telemetry_service_url=TELEMETRY_SERVICE_URL
        )
        
        await alert_manager.initialize()
        logger.info("Alert Service initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing alert service: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Limpiar recursos al cerrar"""
    logger.info("Shutting down Alert Service")


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "service": "SmartHydro Alert Service",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now(CHILE_TZ).isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check del servicio"""
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        # Verificar conexiones
        health_status = await alert_manager.health_check()
        
        return {
            "status": "healthy",
            "service": "alert-service",
            "timestamp": datetime.now(CHILE_TZ).isoformat(),
            "connections": health_status
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(CHILE_TZ).isoformat()
            }
        )


@app.get("/ready")
async def readiness_check():
    """Readiness check"""
    if alert_manager:
        return {"status": "ready"}
    else:
        raise HTTPException(status_code=503, detail="Service not ready")


# ============================================================================
# GESTIÓN DE REGLAS DE ALERTA
# ============================================================================

@app.post("/alerts/rules")
async def create_alert_rule(
    rule: AlertRule,
    current_user: Dict = Depends(get_current_user)
):
    """
    Crear una nueva regla de alerta
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        rule_id = await alert_manager.create_alert_rule(rule)
        
        return {
            "message": "Alert rule created successfully",
            "rule_id": rule_id,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error creating alert rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts/rules")
async def get_alert_rules(
    module: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener reglas de alerta
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        rules = await alert_manager.get_alert_rules(module, is_active)
        
        return {
            "rules": rules,
            "count": len(rules),
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting alert rules: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts/rules/{rule_id}")
async def get_alert_rule(
    rule_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener una regla de alerta específica
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        rule = await alert_manager.get_alert_rule(rule_id)
        
        if not rule:
            raise HTTPException(status_code=404, detail="Alert rule not found")
        
        return {
            "rule": rule,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting alert rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/alerts/rules/{rule_id}")
async def update_alert_rule(
    rule_id: int,
    rule: AlertRule,
    current_user: Dict = Depends(get_current_user)
):
    """
    Actualizar una regla de alerta
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        success = await alert_manager.update_alert_rule(rule_id, rule)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert rule not found")
        
        return {
            "message": "Alert rule updated successfully",
            "rule_id": rule_id,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error updating alert rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/alerts/rules/{rule_id}")
async def delete_alert_rule(
    rule_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """
    Eliminar una regla de alerta
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        success = await alert_manager.delete_alert_rule(rule_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert rule not found")
        
        return {
            "message": "Alert rule deleted successfully",
            "rule_id": rule_id,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error deleting alert rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/alerts/rules/{rule_id}/activate")
async def activate_alert_rule(
    rule_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """
    Activar una regla de alerta
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        success = await alert_manager.activate_alert_rule(rule_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert rule not found")
        
        return {
            "message": "Alert rule activated successfully",
            "rule_id": rule_id,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error activating alert rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/alerts/rules/{rule_id}/deactivate")
async def deactivate_alert_rule(
    rule_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """
    Desactivar una regla de alerta
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        success = await alert_manager.deactivate_alert_rule(rule_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert rule not found")
        
        return {
            "message": "Alert rule deactivated successfully",
            "rule_id": rule_id,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error deactivating alert rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# EJECUCIÓN DE ALERTAS
# ============================================================================

@app.post("/alerts/execute")
async def execute_alert_rule(
    rule_id: int,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """
    Ejecutar una regla de alerta manualmente
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        # Ejecutar en background
        background_tasks.add_task(
            alert_manager.execute_alert_rule,
            rule_id
        )
        
        return {
            "message": "Alert rule execution queued",
            "rule_id": rule_id,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error executing alert rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/alerts/execute-all")
async def execute_all_alert_rules(
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """
    Ejecutar todas las reglas de alerta activas
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        # Ejecutar en background
        background_tasks.add_task(
            alert_manager.execute_all_alert_rules
        )
        
        return {
            "message": "All alert rules execution queued",
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error executing all alert rules: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts/executions")
async def get_alert_executions(
    rule_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener historial de ejecuciones de alertas
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        executions = await alert_manager.get_alert_executions(
            rule_id, status, limit, offset
        )
        
        return {
            "executions": executions,
            "count": len(executions),
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting alert executions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# VARIABLES Y DATOS
# ============================================================================

@app.post("/variables/data")
async def send_variable_data(
    data: VariableData,
    current_user: Dict = Depends(get_current_user)
):
    """
    Enviar datos de variables para evaluación de alertas
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        # Procesar datos de variables
        await alert_manager.process_variable_data(data)
        
        return {
            "message": "Variable data processed successfully",
            "variable": data.variable_name,
            "value": data.value,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing variable data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/variables/available")
async def get_available_variables(
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener variables disponibles para alertas
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        variables = await alert_manager.get_available_variables()
        
        return {
            "variables": variables,
            "count": len(variables),
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting available variables: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/variables/{variable_name}/history")
async def get_variable_history(
    variable_name: str,
    hours: int = 24,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener historial de una variable específica
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        history = await alert_manager.get_variable_history(variable_name, hours)
        
        return {
            "variable": variable_name,
            "history": history,
            "count": len(history),
            "hours": hours,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting variable history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CONDICIONES Y OPERADORES
# ============================================================================

@app.get("/conditions/operators")
async def get_available_operators():
    """
    Obtener operadores disponibles para condiciones
    """
    operators = [
        {"value": "eq", "label": "Igual a (=)", "description": "Valor igual al especificado"},
        {"value": "ne", "label": "Diferente a (≠)", "description": "Valor diferente al especificado"},
        {"value": "gt", "label": "Mayor que (>)", "description": "Valor mayor al especificado"},
        {"value": "gte", "label": "Mayor o igual que (≥)", "description": "Valor mayor o igual al especificado"},
        {"value": "lt", "label": "Menor que (<)", "description": "Valor menor al especificado"},
        {"value": "lte", "label": "Menor o igual que (≤)", "description": "Valor menor o igual al especificado"},
        {"value": "contains", "label": "Contiene", "description": "Valor contiene el texto especificado"},
        {"value": "not_contains", "label": "No contiene", "description": "Valor no contiene el texto especificado"},
        {"value": "in", "label": "Está en lista", "description": "Valor está en la lista especificada"},
        {"value": "not_in", "label": "No está en lista", "description": "Valor no está en la lista especificada"},
        {"value": "between", "label": "Entre valores", "description": "Valor está entre dos valores especificados"},
        {"value": "is_null", "label": "Es nulo", "description": "Valor es nulo o vacío"},
        {"value": "is_not_null", "label": "No es nulo", "description": "Valor no es nulo ni vacío"}
    ]
    
    return {
        "operators": operators,
        "count": len(operators),
        "timestamp": datetime.now(CHILE_TZ).isoformat()
    }


@app.get("/conditions/functions")
async def get_available_functions():
    """
    Obtener funciones disponibles para condiciones
    """
    functions = [
        {"value": "avg", "label": "Promedio", "description": "Promedio de valores en el período"},
        {"value": "sum", "label": "Suma", "description": "Suma de valores en el período"},
        {"value": "min", "label": "Mínimo", "description": "Valor mínimo en el período"},
        {"value": "max", "label": "Máximo", "description": "Valor máximo en el período"},
        {"value": "count", "label": "Conteo", "description": "Número de valores en el período"},
        {"value": "std", "label": "Desviación estándar", "description": "Desviación estándar de valores"},
        {"value": "trend", "label": "Tendencia", "description": "Tendencia de valores (creciente/decreciente)"},
        {"value": "change", "label": "Cambio", "description": "Cambio porcentual respecto al valor anterior"}
    ]
    
    return {
        "functions": functions,
        "count": len(functions),
        "timestamp": datetime.now(CHILE_TZ).isoformat()
    }


# ============================================================================
# MÓDULOS Y TIPOS DE ALERTA
# ============================================================================

@app.get("/modules")
async def get_available_modules():
    """
    Obtener módulos disponibles para alertas
    """
    modules = [
        {"value": "telemetry", "label": "Telemetría", "description": "Alertas basadas en datos de sensores"},
        {"value": "banking", "label": "Banking", "description": "Alertas financieras y bancarias"},
        {"value": "payments", "label": "Payments", "description": "Alertas de pagos y transacciones"},
        {"value": "quotations", "label": "Quotations", "description": "Alertas de cotizaciones"},
        {"value": "support", "label": "Support", "description": "Alertas de soporte y tickets"},
        {"value": "projects", "label": "Projects", "description": "Alertas de proyectos"},
        {"value": "system", "label": "System", "description": "Alertas del sistema"},
        {"value": "custom", "label": "Custom", "description": "Alertas personalizadas"}
    ]
    
    return {
        "modules": modules,
        "count": len(modules),
        "timestamp": datetime.now(CHILE_TZ).isoformat()
    }


@app.get("/alert-types")
async def get_alert_types():
    """
    Obtener tipos de alerta disponibles
    """
    alert_types = [
        {"value": "info", "label": "Información", "description": "Alerta informativa", "color": "blue"},
        {"value": "warning", "label": "Advertencia", "description": "Alerta de advertencia", "color": "yellow"},
        {"value": "error", "label": "Error", "description": "Alerta de error", "color": "red"},
        {"value": "critical", "label": "Crítica", "description": "Alerta crítica", "color": "red"},
        {"value": "success", "label": "Éxito", "description": "Alerta de éxito", "color": "green"}
    ]
    
    return {
        "alert_types": alert_types,
        "count": len(alert_types),
        "timestamp": datetime.now(CHILE_TZ).isoformat()
    }


# ============================================================================
# MÉTRICAS Y ESTADÍSTICAS
# ============================================================================

@app.get("/metrics")
async def get_metrics(
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener métricas del servicio de alertas
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        metrics = await alert_manager.get_metrics()
        
        return {
            "metrics": metrics,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts/stats")
async def get_alert_stats(
    days: int = 7,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener estadísticas de alertas
    """
    try:
        if not alert_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        stats = await alert_manager.get_alert_stats(days)
        
        return {
            "stats": stats,
            "days": days,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting alert stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8007,
        reload=True,
        log_level="info"
    ) 