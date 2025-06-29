"""
SmartHydro Notification Service - FastAPI
Microservicio para manejo de notificaciones en tiempo real
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
import uvicorn
import pytz
import httpx

from .notification_manager import NotificationManager
from .models import NotificationRequest, NotificationTemplate, NotificationPreference
from .auth import get_current_user

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de zona horaria
CHILE_TZ = pytz.timezone('America/Santiago')

# Crear aplicación FastAPI
app = FastAPI(
    title="SmartHydro Notification Service",
    description="Microservicio para notificaciones en tiempo real del ERP",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del manager de notificaciones
notification_manager: Optional[NotificationManager] = None

# Configuración de servicios
DJANGO_API_URL = "http://business-api:8004"  # API Django principal


@app.on_event("startup")
async def startup_event():
    """Inicializar el manager de notificaciones al arrancar"""
    global notification_manager
    
    try:
        notification_manager = NotificationManager(
            database_url="postgresql://smarthydro:smarthydro123@postgres:5432/smarthydro_business",
            redis_url="redis://redis:6379",
            django_api_url=DJANGO_API_URL
        )
        
        await notification_manager.initialize()
        logger.info("Notification Service initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing notification service: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Limpiar recursos al cerrar"""
    logger.info("Shutting down Notification Service")


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "service": "SmartHydro Notification Service",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now(CHILE_TZ).isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check del servicio"""
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        # Verificar conexiones
        health_status = await notification_manager.health_check()
        
        return {
            "status": "healthy",
            "service": "notification-service",
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
    if notification_manager:
        return {"status": "ready"}
    else:
        raise HTTPException(status_code=503, detail="Service not ready")


@app.post("/notifications/send")
async def send_notification(
    request: NotificationRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """
    Enviar notificación usando plantilla
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        # Ejecutar en background
        background_tasks.add_task(
            notification_manager.send_notification,
            request.template_name,
            request.module,
            request.user_ids,
            request.context_data,
            request.priority,
            request.related_model,
            request.related_id
        )
        
        return {
            "message": "Notification queued for sending",
            "template": request.template_name,
            "module": request.module,
            "users_count": len(request.user_ids),
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/notifications/send-custom")
async def send_custom_notification(
    subject: str,
    message: str,
    user_ids: List[int],
    priority: str = "medium",
    module: str = "global",
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """
    Enviar notificación personalizada sin plantilla
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        # Ejecutar en background
        background_tasks.add_task(
            notification_manager.send_custom_notification,
            subject,
            message,
            user_ids,
            priority,
            module
        )
        
        return {
            "message": "Custom notification queued for sending",
            "subject": subject,
            "users_count": len(user_ids),
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error sending custom notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notifications/user/{user_id}")
async def get_user_notifications(
    user_id: int,
    status: Optional[str] = None,
    module: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener notificaciones de un usuario específico
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        notifications = await notification_manager.get_user_notifications(
            user_id, status, module, limit, offset
        )
        
        return {
            "notifications": notifications,
            "user_id": user_id,
            "count": len(notifications),
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting user notifications: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/notifications/{notification_id}/mark-read")
async def mark_notification_read(
    notification_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """
    Marcar notificación como leída
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        success = await notification_manager.mark_notification_read(notification_id)
        
        if success:
            return {
                "message": "Notification marked as read",
                "notification_id": notification_id,
                "timestamp": datetime.now(CHILE_TZ).isoformat()
            }
        else:
            raise HTTPException(status_code=404, detail="Notification not found")
            
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/notifications/user/{user_id}/mark-all-read")
async def mark_all_notifications_read(
    user_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """
    Marcar todas las notificaciones de un usuario como leídas
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        count = await notification_manager.mark_all_notifications_read(user_id)
        
        return {
            "message": f"{count} notifications marked as read",
            "user_id": user_id,
            "count": count,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error marking all notifications as read: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notifications/user/{user_id}/unread-count")
async def get_unread_count(
    user_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener conteo de notificaciones no leídas
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        count = await notification_manager.get_unread_count(user_id)
        
        return {
            "user_id": user_id,
            "unread_count": count,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting unread count: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notifications/user/{user_id}/stats")
async def get_user_notification_stats(
    user_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener estadísticas de notificaciones de un usuario
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        stats = await notification_manager.get_user_notification_stats(user_id)
        
        return {
            "user_id": user_id,
            "stats": stats,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting notification stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/templates")
async def get_templates(
    module: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener plantillas de notificación
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        templates = await notification_manager.get_templates(module)
        
        return {
            "templates": templates,
            "module": module,
            "count": len(templates),
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/preferences/user/{user_id}")
async def get_user_preferences(
    user_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtener preferencias de notificación de un usuario
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        preferences = await notification_manager.get_user_preferences(user_id)
        
        return {
            "user_id": user_id,
            "preferences": preferences,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting user preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/preferences/user/{user_id}")
async def update_user_preferences(
    user_id: int,
    preferences: Dict[str, Any],
    current_user: Dict = Depends(get_current_user)
):
    """
    Actualizar preferencias de notificación de un usuario
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        success = await notification_manager.update_user_preferences(user_id, preferences)
        
        if success:
            return {
                "message": "Preferences updated successfully",
                "user_id": user_id,
                "timestamp": datetime.now(CHILE_TZ).isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid preferences")
            
    except Exception as e:
        logger.error(f"Error updating user preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/modules")
async def get_available_modules():
    """
    Obtener módulos disponibles para notificaciones
    """
    modules = [
        {"value": "banking", "label": "Banking"},
        {"value": "payments", "label": "Payments"},
        {"value": "quotations", "label": "Quotations"},
        {"value": "invoicing", "label": "Invoicing"},
        {"value": "support", "label": "Support"},
        {"value": "projects", "label": "Projects"},
        {"value": "global", "label": "Global"}
    ]
    
    return {
        "modules": modules,
        "count": len(modules),
        "timestamp": datetime.now(CHILE_TZ).isoformat()
    }


@app.get("/metrics")
async def get_metrics():
    """
    Obtener métricas del servicio de notificaciones
    """
    try:
        if not notification_manager:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        metrics = await notification_manager.get_metrics()
        
        return {
            "metrics": metrics,
            "timestamp": datetime.now(CHILE_TZ).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
        log_level="info"
    ) 