"""
Serializers Frontend para API Externa
Proporciona serializers con lógica específica para frontend
"""
from rest_framework import serializers
from django.core.cache import cache
from api.apps.core.api.base.serializers.base_serializers import (
    VariableBaseSerializer,
    VariableSchemaBaseSerializer,
    CatchmentPointBaseSerializer,
    TelemetryDataBaseSerializer
)


class VariableFrontendSerializer(VariableBaseSerializer):
    """Serializer para frontend con campos adicionales"""
    
    # Campos adicionales para frontend
    display_name = serializers.SerializerMethodField()
    unit_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    variable_type_display = serializers.SerializerMethodField()
    
    def get_display_name(self, obj):
        """Obtener nombre para mostrar (con label personalizado)"""
        # Aquí puedes implementar lógica para obtener labels personalizados
        # Por ejemplo, desde configuración de usuario o punto de captación
        return obj.name
    
    def get_unit_display(self, obj):
        """Obtener unidad formateada para frontend"""
        if obj.unit == 'CUSTOM' and obj.custom_unit:
            return obj.custom_unit
        return obj.get_unit_display()
    
    def get_status_display(self, obj):
        """Obtener estado formateado para frontend"""
        return "Activa" if obj.is_active else "Inactiva"
    
    def get_variable_type_display(self, obj):
        """Obtener tipo de variable formateado"""
        return obj.get_variable_type_display()


class VariableSchemaFrontendSerializer(VariableSchemaBaseSerializer):
    """Serializer para frontend con esquemas"""
    
    # Campos adicionales para frontend
    variables_count = serializers.SerializerMethodField()
    is_configured = serializers.SerializerMethodField()
    variables_detail = serializers.SerializerMethodField()
    
    def get_variables_count(self, obj):
        """Contar variables en el esquema"""
        return len(obj.variables) if obj.variables else 0
    
    def get_is_configured(self, obj):
        """Verificar si el esquema está configurado"""
        return bool(obj.config and obj.variables)
    
    def get_variables_detail(self, obj):
        """Obtener detalles de las variables del esquema"""
        if not obj.variables:
            return []
        
        # Aquí podrías hacer una consulta para obtener detalles de las variables
        # Por ahora retornamos la información básica
        return obj.variables


class CatchmentPointFrontendSerializer(CatchmentPointBaseSerializer):
    """Serializer para frontend con puntos de captación"""
    
    # Campos adicionales para frontend
    point_type_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    location_display = serializers.SerializerMethodField()
    variables_count = serializers.SerializerMethodField()
    
    def get_point_type_display(self, obj):
        """Obtener tipo de punto formateado"""
        return obj.get_point_type_display()
    
    def get_status_display(self, obj):
        """Obtener estado formateado"""
        return obj.get_status_display()
    
    def get_location_display(self, obj):
        """Obtener ubicación formateada"""
        return obj.location_display
    
    def get_variables_count(self, obj):
        """Contar variables configuradas para este punto"""
        # Aquí podrías implementar la lógica para contar variables
        # Por ahora retornamos 0
        return 0


class TelemetryDataFrontendSerializer(TelemetryDataBaseSerializer):
    """Serializer para frontend con datos de telemetría"""
    
    # Campos adicionales para frontend
    catchment_point_name = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    formatted_values = serializers.SerializerMethodField()
    
    def get_catchment_point_name(self, obj):
        """Obtener nombre del punto de captación"""
        return obj.catchment_point.name if obj.catchment_point else "N/A"
    
    def get_time_ago(self, obj):
        """Obtener tiempo transcurrido desde la medición"""
        from django.utils import timezone
        from datetime import datetime
        
        if obj.measurement_time:
            now = timezone.now()
            diff = now - obj.measurement_time
            
            if diff.days > 0:
                return f"{diff.days} días"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} horas"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minutos"
            else:
                return "Ahora mismo"
        
        return "N/A"
    
    def get_status_display(self, obj):
        """Obtener estado formateado"""
        if obj.is_error:
            return "Error"
        elif obj.is_warning:
            return "Advertencia"
        else:
            return "Normal"
    
    def get_formatted_values(self, obj):
        """Obtener valores formateados para frontend"""
        formatted = {}
        
        if obj.level is not None:
            formatted['level'] = f"{obj.level:.2f} m"
        
        if obj.water_table is not None:
            formatted['water_table'] = f"{obj.water_table:.2f} m"
        
        if obj.flow is not None:
            formatted['flow'] = f"{obj.flow:.2f} L/s"
        
        if obj.temperature is not None:
            formatted['temperature'] = f"{obj.temperature:.1f} °C"
        
        if obj.pressure is not None:
            formatted['pressure'] = f"{obj.pressure:.2f} Bar"
        
        if obj.ph is not None:
            formatted['ph'] = f"{obj.ph:.1f} pH"
        
        if obj.conductivity is not None:
            formatted['conductivity'] = f"{obj.conductivity:.0f} μS/cm"
        
        if obj.turbidity is not None:
            formatted['turbidity'] = f"{obj.turbidity:.1f} NTU"
        
        if obj.battery_level is not None:
            formatted['battery_level'] = f"{obj.battery_level:.0f}%"
        
        return formatted 