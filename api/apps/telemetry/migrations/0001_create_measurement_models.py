"""
Migración inicial para modelos unificados de mediciones
"""
from django.db import migrations, models
import django.db.models.deletion
from django.contrib.postgres.indexes import GinIndex


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('telemetry', '0001_initial'),  # Asegúrate de que esta sea la migración correcta
    ]

    operations = [
        # Crear tabla de mediciones unificadas
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('timestamp', models.DateTimeField(db_index=True, verbose_name='Timestamp de medición')),
                ('value_numeric', models.DecimalField(blank=True, decimal_places=6, max_digits=15, null=True, verbose_name='Valor numérico')),
                ('value_text', models.TextField(blank=True, null=True, verbose_name='Valor de texto')),
                ('value_boolean', models.BooleanField(blank=True, null=True, verbose_name='Valor booleano')),
                ('raw_value', models.JSONField(default=dict, help_text='Valor original del proveedor', verbose_name='Valor original')),
                ('quality_score', models.FloatField(default=1.0, help_text='Puntuación de calidad (0.0 - 1.0)', verbose_name='Puntuación de calidad')),
                ('provider', models.CharField(max_length=50, verbose_name='Proveedor')),
                ('processing_config', models.JSONField(default=dict, help_text='Configuración aplicada durante el procesamiento', verbose_name='Configuración de procesamiento')),
                ('days_since_last_connection', models.IntegerField(default=0, verbose_name='Días desde última conexión')),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='telemetry.catchmentpoint', verbose_name='Punto de captación')),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='telemetry.variable', verbose_name='Variable')),
            ],
            options={
                'verbose_name': 'Medición',
                'verbose_name_plural': 'Mediciones',
                'db_table': 'telemetry_measurement',
                'ordering': ['-timestamp'],
            },
        ),
        
        # Crear tabla de lotes de mediciones
        migrations.CreateModel(
            name='MeasurementBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('batch_id', models.CharField(max_length=100, unique=True, verbose_name='ID del lote')),
                ('provider', models.CharField(max_length=50, verbose_name='Proveedor')),
                ('frequency', models.CharField(max_length=10, verbose_name='Frecuencia')),
                ('total_measurements', models.IntegerField(default=0, verbose_name='Total de mediciones')),
                ('processed_measurements', models.IntegerField(default=0, verbose_name='Mediciones procesadas')),
                ('failed_measurements', models.IntegerField(default=0, verbose_name='Mediciones fallidas')),
                ('processing_time_ms', models.IntegerField(blank=True, null=True, verbose_name='Tiempo de procesamiento (ms)')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('processing', 'Procesando'), ('completed', 'Completado'), ('failed', 'Fallido')], default='pending', max_length=20, verbose_name='Estado')),
                ('metadata', models.JSONField(default=dict, verbose_name='Metadatos')),
            ],
            options={
                'verbose_name': 'Lote de Mediciones',
                'verbose_name_plural': 'Lotes de Mediciones',
                'db_table': 'telemetry_measurement_batch',
                'ordering': ['-created_at'],
            },
        ),
        
        # Crear tabla de métricas de calidad
        migrations.CreateModel(
            name='MeasurementQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('outlier_score', models.FloatField(default=0.0, help_text='Puntuación de outlier (0.0 - 1.0)', verbose_name='Puntuación de outlier')),
                ('consistency_score', models.FloatField(default=1.0, help_text='Puntuación de consistencia (0.0 - 1.0)', verbose_name='Puntuación de consistencia')),
                ('completeness_score', models.FloatField(default=1.0, help_text='Puntuación de completitud (0.0 - 1.0)', verbose_name='Puntuación de completitud')),
                ('is_outlier', models.BooleanField(default=False, verbose_name='Es outlier')),
                ('is_missing', models.BooleanField(default=False, verbose_name='Falta dato')),
                ('is_interpolated', models.BooleanField(default=False, verbose_name='Es interpolado')),
                ('quality_notes', models.TextField(blank=True, verbose_name='Notas de calidad')),
                ('measurement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quality_metrics', to='telemetry.measurement', verbose_name='Medición')),
            ],
            options={
                'verbose_name': 'Métrica de Calidad',
                'verbose_name_plural': 'Métricas de Calidad',
                'db_table': 'telemetry_measurement_quality',
            },
        ),
        
        # Crear índices optimizados
        migrations.AddIndex(
            model_name='measurement',
            index=models.Index(fields=['point', 'variable', '-timestamp'], name='measurement_point_var_time_idx'),
        ),
        migrations.AddIndex(
            model_name='measurement',
            index=models.Index(fields=['timestamp'], name='measurement_timestamp_idx'),
        ),
        migrations.AddIndex(
            model_name='measurement',
            index=models.Index(fields=['provider', '-timestamp'], name='measurement_provider_time_idx'),
        ),
        migrations.AddIndex(
            model_name='measurement',
            index=models.Index(fields=['variable', '-timestamp'], name='measurement_variable_time_idx'),
        ),
        
        # Índices GIN para JSON
        migrations.AddIndex(
            model_name='measurement',
            index=GinIndex(fields=['raw_value'], name='measurement_raw_value_gin_idx'),
        ),
        migrations.AddIndex(
            model_name='measurement',
            index=GinIndex(fields=['processing_config'], name='measurement_processing_config_gin_idx'),
        ),
        
        # Restricción única para evitar duplicados
        migrations.AddConstraint(
            model_name='measurement',
            constraint=models.UniqueConstraint(fields=['point', 'variable', 'timestamp'], name='unique_measurement_point_var_time'),
        ),
    ] 