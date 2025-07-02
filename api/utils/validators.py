"""
Utilidades de validación
"""
import re
from typing import Any, Dict, List
from datetime import datetime


def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Valida formato de teléfono"""
    # Patrón para teléfonos chilenos
    pattern = r'^\+?56?[29][0-9]{8}$'
    return bool(re.match(pattern, phone))


def validate_coordinates(lat: float, lon: float) -> bool:
    """Valida coordenadas geográficas"""
    return -90 <= lat <= 90 and -180 <= lon <= 180


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Valida datos contra un esquema JSON"""
    try:
        required_fields = schema.get('required', [])
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Validar tipos de campos
        for field, field_schema in schema.get('properties', {}).items():
            if field in data:
                field_type = field_schema.get('type')
                if field_type == 'string' and not isinstance(data[field], str):
                    return False
                elif field_type == 'number' and not isinstance(data[field], (int, float)):
                    return False
                elif field_type == 'boolean' and not isinstance(data[field], bool):
                    return False
        
        return True
        
    except Exception:
        return False


def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
    """Valida rango de fechas"""
    return start_date < end_date


def sanitize_string(text: str) -> str:
    """Sanitiza string para evitar inyección"""
    # Remover caracteres peligrosos
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Valida configuración del sistema"""
    errors = []
    
    # Validar campos requeridos
    required_fields = ['name', 'type', 'enabled']
    for field in required_fields:
        if field not in config:
            errors.append(f"Campo requerido '{field}' no encontrado")
    
    # Validar tipos
    if 'enabled' in config and not isinstance(config['enabled'], bool):
        errors.append("Campo 'enabled' debe ser booleano")
    
    if 'name' in config and not isinstance(config['name'], str):
        errors.append("Campo 'name' debe ser string")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }