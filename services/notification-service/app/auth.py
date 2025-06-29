"""
Módulo de autenticación para el servicio de notificaciones
"""
import logging
from typing import Dict, Optional
import httpx
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

# Configuración
DJANGO_API_URL = "http://business-api:8004"
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Verificar token y obtener usuario actual
    """
    try:
        token = credentials.credentials
        
        # Verificar token con Django API
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{DJANGO_API_URL}/users/me/", headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                return user_data
            else:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication credentials"
                )
                
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )


async def verify_user_permission(user_id: int, current_user: Dict) -> bool:
    """
    Verificar si el usuario actual puede acceder a datos de otro usuario
    """
    # Administradores pueden acceder a todo
    if current_user.get('is_staff') or current_user.get('is_superuser'):
        return True
    
    # Usuarios solo pueden acceder a sus propios datos
    return current_user.get('id') == user_id


async def require_admin(current_user: Dict = Depends(get_current_user)) -> Dict:
    """
    Requerir que el usuario sea administrador
    """
    if not current_user.get('is_staff') and not current_user.get('is_superuser'):
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    return current_user 