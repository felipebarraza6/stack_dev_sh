from django.contrib import admin
from api.apps.telemetry.models.models import (
    TelemetryData,
    RawTelemetryData,
    ProcessedTelemetryData,
    TelemetryProcessingLog
)
from api.apps.telemetry.models.schemas.response_schema import ResponseSchema

@admin.register(RawTelemetryData)
class RawTelemetryDataAdmin(admin.ModelAdmin):
    list_display = ('catchment_point', 'measurement_time', 'is_processed', 'processing_status')
    list_filter = ('catchment_point', 'is_processed', 'processing_status')
    search_fields = ('catchment_point__name',)
    date_hierarchy = 'measurement_time'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ResponseSchema)
class ResponseSchemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema_type', 'is_active', 'created_at')
    list_filter = ('schema_type', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

# @admin.register(ProcessingConstant)  # Comentado porque no existe el modelo
# class ProcessingConstantAdmin(admin.ModelAdmin):
#     list_display = ('name', 'constant_type', 'value', 'start_date', 'end_date', 'is_active')
#     list_filter = ('constant_type', 'is_active')
#     search_fields = ('name',)
#     filter_horizontal = ('catchment_points', 'variables')
#     readonly_fields = ('created_at', 'updated_at')
#     date_hierarchy = 'start_date'

@admin.register(ProcessedTelemetryData)
class ProcessedTelemetryDataAdmin(admin.ModelAdmin):
    list_display = ('catchment_point', 'response_schema', 'measurement_time', 'processing_status')
    list_filter = ('catchment_point', 'response_schema', 'processing_status')
    search_fields = ('catchment_point__name', 'response_schema__name')
    date_hierarchy = 'measurement_time'
    readonly_fields = ('created_at', 'updated_at')

 