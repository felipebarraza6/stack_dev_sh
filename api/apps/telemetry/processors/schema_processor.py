"""
Procesador de Esquemas de Telemetría
Sistema para agrupar datos según esquemas dinámicos
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from django.db.models import Q, Avg, Max, Min, Sum, Count
from django.utils import timezone

from .models_schemas import TelemetrySchema, TelemetryGroup, TelemetrySchemaMapping
from api.apps.variables.models import VariableDataPoint, Variable
from api.apps.catchment.models import CatchmentPoint

logger = logging.getLogger(__name__)


class SchemaProcessor:
    """Procesador principal de esquemas de telemetría"""
    
    def __init__(self, schema: TelemetrySchema):
        self.schema = schema
        self.config = schema.get_grouping_config()
    
    def process_schema(self, catchment_point_id: Optional[int] = None, 
                      start_time: Optional[datetime] = None,
                      end_time: Optional[datetime] = None) -> List[TelemetryGroup]:
        """
        Procesar esquema para generar grupos de datos
        
        Args:
            catchment_point_id: ID del punto de captación (opcional)
            start_time: Tiempo de inicio (opcional)
            end_time: Tiempo de fin (opcional)
        
        Returns:
            Lista de grupos de telemetría creados
        """
        try:
            # Obtener puntos de captación a procesar
            points = self._get_catchment_points(catchment_point_id)
            
            # Obtener variables del esquema
            variables = self.schema.variables.all()
            
            # Procesar cada punto
            groups_created = []
            for point in points:
                groups = self._process_point(point, variables, start_time, end_time)
                groups_created.extend(groups)
            
            logger.info(f"Procesado esquema '{self.schema.name}': {len(groups_created)} grupos creados")
            return groups_created
            
        except Exception as e:
            logger.error(f"Error procesando esquema '{self.schema.name}': {str(e)}")
            raise
    
    def _get_catchment_points(self, catchment_point_id: Optional[int] = None) -> List[CatchmentPoint]:
        """Obtener puntos de captación a procesar"""
        if catchment_point_id:
            return [CatchmentPoint.objects.get(id=catchment_point_id)]
        
        # Obtener puntos mapeados a este esquema
        mappings = TelemetrySchemaMapping.objects.filter(
            schema=self.schema,
            is_active=True
        ).select_related('catchment_point')
        
        return [mapping.catchment_point for mapping in mappings]
    
    def _process_point(self, point: CatchmentPoint, variables: List[Variable],
                      start_time: Optional[datetime], end_time: Optional[datetime]) -> List[TelemetryGroup]:
        """Procesar un punto de captación específico"""
        groups = []
        
        # Obtener datos de variables para este punto
        data_points = self._get_data_points(point.id, variables, start_time, end_time)
        
        if not data_points:
            return groups
        
        # Agrupar por ventana de tiempo
        time_windows = self._create_time_windows(data_points)
        
        for window_start, window_end in time_windows:
            # Agrupar datos en esta ventana
            grouped_data = self._group_data_in_window(
                data_points, window_start, window_end, variables
            )
            
            if grouped_data:
                # Crear grupo de telemetría
                group = self._create_telemetry_group(
                    point, window_start, grouped_data
                )
                groups.append(group)
        
        return groups
    
    def _get_data_points(self, point_id: int, variables: List[Variable],
                        start_time: Optional[datetime], end_time: Optional[datetime]) -> List[VariableDataPoint]:
        """Obtener puntos de datos para las variables del esquema"""
        query = VariableDataPoint.objects.filter(
            catchment_point_id=point_id,
            variable__in=variables
        )
        
        if start_time:
            query = query.filter(timestamp__gte=start_time)
        if end_time:
            query = query.filter(timestamp__lte=end_time)
        
        return list(query.select_related('variable').order_by('timestamp'))
    
    def _create_time_windows(self, data_points: List[VariableDataPoint]) -> List[tuple]:
        """Crear ventanas de tiempo según configuración"""
        if not data_points:
            return []
        
        time_window = self.config.get('time_window', '1_hour')
        start_time = min(dp.timestamp for dp in data_points)
        end_time = max(dp.timestamp for dp in data_points)
        
        windows = []
        current_time = start_time
        
        while current_time <= end_time:
            window_end = self._add_time_window(current_time, time_window)
            windows.append((current_time, window_end))
            current_time = window_end
        
        return windows
    
    def _add_time_window(self, time: datetime, window: str) -> datetime:
        """Agregar ventana de tiempo"""
        if window == '1_minute':
            return time + timedelta(minutes=1)
        elif window == '5_minutes':
            return time + timedelta(minutes=5)
        elif window == '15_minutes':
            return time + timedelta(minutes=15)
        elif window == '30_minutes':
            return time + timedelta(minutes=30)
        elif window == '1_hour':
            return time + timedelta(hours=1)
        elif window == '6_hours':
            return time + timedelta(hours=6)
        elif window == '12_hours':
            return time + timedelta(hours=12)
        elif window == '1_day':
            return time + timedelta(days=1)
        else:
            return time + timedelta(hours=1)  # Default
    
    def _group_data_in_window(self, data_points: List[VariableDataPoint],
                             window_start: datetime, window_end: datetime,
                             variables: List[Variable]) -> Dict[str, Any]:
        """Agrupar datos en una ventana de tiempo específica"""
        # Filtrar datos en la ventana
        window_data = [
            dp for dp in data_points
            if window_start <= dp.timestamp < window_end
        ]
        
        if not window_data:
            return {}
        
        # Agrupar por variable
        grouped_data = {}
        aggregation = self.config.get('aggregation', 'average')
        
        for variable in variables:
            var_data = [dp for dp in window_data if dp.variable == variable]
            
            if var_data:
                grouped_data[variable.code] = self._aggregate_data(var_data, aggregation)
        
        return grouped_data
    
    def _aggregate_data(self, data_points: List[VariableDataPoint], 
                       aggregation: str) -> Dict[str, Any]:
        """Agregar datos según el tipo de agregación"""
        if not data_points:
            return {}
        
        values = [dp.value for dp in data_points]
        timestamps = [dp.timestamp for dp in data_points]
        
        result = {
            'count': len(data_points),
            'timestamps': [ts.isoformat() for ts in timestamps],
            'quality': self._get_quality_summary(data_points)
        }
        
        if aggregation == 'average':
            result['value'] = sum(values) / len(values)
        elif aggregation == 'sum':
            result['value'] = sum(values)
        elif aggregation == 'min':
            result['value'] = min(values)
        elif aggregation == 'max':
            result['value'] = max(values)
        elif aggregation == 'latest':
            result['value'] = values[-1]
        elif aggregation == 'first':
            result['value'] = values[0]
        else:
            result['value'] = sum(values) / len(values)  # Default to average
        
        return result
    
    def _get_quality_summary(self, data_points: List[VariableDataPoint]) -> Dict[str, int]:
        """Obtener resumen de calidad de datos"""
        quality_counts = {}
        for dp in data_points:
            quality_counts[dp.quality] = quality_counts.get(dp.quality, 0) + 1
        return quality_counts
    
    def _create_telemetry_group(self, point: CatchmentPoint, timestamp: datetime,
                               grouped_data: Dict[str, Any]) -> TelemetryGroup:
        """Crear grupo de telemetría"""
        # Calcular campos adicionales
        calculated_fields = self._calculate_fields(grouped_data)
        
        # Crear metadata de agrupación
        grouping_metadata = {
            'schema_name': self.schema.name,
            'schema_type': self.schema.schema_type,
            'time_window': self.config.get('time_window'),
            'aggregation': self.config.get('aggregation'),
            'variables_count': len(grouped_data),
            'processed_at': timezone.now().isoformat()
        }
        
        # Crear o actualizar grupo
        group, created = TelemetryGroup.objects.update_or_create(
            schema=self.schema,
            catchment_point=point,
            timestamp=timestamp,
            defaults={
                'grouped_data': grouped_data,
                'calculated_fields': calculated_fields,
                'grouping_metadata': grouping_metadata,
                'processing_status': 'COMPLETED'
            }
        )
        
        if created:
            logger.debug(f"Grupo creado: {group}")
        else:
            logger.debug(f"Grupo actualizado: {group}")
        
        return group
    
    def _calculate_fields(self, grouped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcular campos adicionales según esquema"""
        calculated_fields = {}
        
        # Obtener campos calculados del esquema
        schema_calculated = self.schema.calculated_fields or []
        
        for field_config in schema_calculated:
            field_name = field_config.get('name')
            field_type = field_config.get('type')
            field_config = field_config.get('config', {})
            
            if field_name and field_type:
                calculated_fields[field_name] = self._calculate_field(
                    field_type, field_config, grouped_data
                )
        
        return calculated_fields
    
    def _calculate_field(self, field_type: str, config: Dict[str, Any],
                        grouped_data: Dict[str, Any]) -> Any:
        """Calcular un campo específico"""
        if field_type == 'sum':
            variables = config.get('variables', [])
            return sum(
                grouped_data.get(var, {}).get('value', 0)
                for var in variables
            )
        
        elif field_type == 'average':
            variables = config.get('variables', [])
            values = [
                grouped_data.get(var, {}).get('value', 0)
                for var in variables
            ]
            return sum(values) / len(values) if values else 0
        
        elif field_type == 'ratio':
            numerator = grouped_data.get(config.get('numerator'), {}).get('value', 0)
            denominator = grouped_data.get(config.get('denominator'), {}).get('value', 1)
            return numerator / denominator if denominator != 0 else 0
        
        elif field_type == 'custom':
            # Aquí se podría ejecutar código personalizado
            return config.get('default_value', 0)
        
        return 0


class SchemaManager:
    """Gestor de esquemas de telemetría"""
    
    @staticmethod
    def get_schema_by_name(name: str) -> Optional[TelemetrySchema]:
        """Obtener esquema por nombre"""
        try:
            return TelemetrySchema.objects.get(name=name, is_active=True)
        except TelemetrySchema.DoesNotExist:
            return None
    
    @staticmethod
    def get_schemas_by_type(schema_type: str) -> List[TelemetrySchema]:
        """Obtener esquemas por tipo"""
        return list(TelemetrySchema.objects.filter(
            schema_type=schema_type,
            is_active=True
        ))
    
    @staticmethod
    def process_all_schemas(catchment_point_id: Optional[int] = None,
                           schema_type: Optional[str] = None) -> Dict[str, int]:
        """Procesar todos los esquemas activos"""
        schemas = TelemetrySchema.objects.filter(is_active=True)
        
        if schema_type:
            schemas = schemas.filter(schema_type=schema_type)
        
        results = {}
        for schema in schemas:
            try:
                processor = SchemaProcessor(schema)
                groups = processor.process_schema(catchment_point_id)
                results[schema.name] = len(groups)
            except Exception as e:
                logger.error(f"Error procesando esquema {schema.name}: {str(e)}")
                results[schema.name] = 0
        
        return results
    
    @staticmethod
    def create_default_schemas():
        """Crear esquemas por defecto"""
        default_schemas = [
            {
                'name': 'Medición Básica',
                'schema_type': 'MEASUREMENT',
                'description': 'Esquema básico para mediciones de caudal y nivel',
                'grouping_config': {
                    'time_window': '1_hour',
                    'aggregation': 'average'
                },
                'calculated_fields': [
                    {
                        'name': 'consumo_hora',
                        'type': 'sum',
                        'config': {'variables': ['flow']}
                    }
                ]
            },
            {
                'name': 'Dashboard Principal',
                'schema_type': 'DASHBOARD',
                'description': 'Esquema para dashboard principal',
                'grouping_config': {
                    'time_window': '15_minutes',
                    'aggregation': 'latest'
                }
            },
            {
                'name': 'Reporte Diario',
                'schema_type': 'REPORT',
                'description': 'Esquema para reportes diarios',
                'grouping_config': {
                    'time_window': '1_day',
                    'aggregation': 'sum'
                }
            }
        ]
        
        for schema_data in default_schemas:
            schema, created = TelemetrySchema.objects.get_or_create(
                name=schema_data['name'],
                defaults=schema_data
            )
            if created:
                logger.info(f"Esquema creado: {schema.name}")
            else:
                logger.info(f"Esquema ya existe: {schema.name}")
        
        return TelemetrySchema.objects.filter(is_active=True) 