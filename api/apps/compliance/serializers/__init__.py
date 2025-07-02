"""
Serializers de Cumplimiento
"""
from rest_framework import serializers

from .sources import (
    ComplianceSourceSerializer,
    ComplianceSourceListSerializer,
    ComplianceSourceDetailSerializer,
)

from .configs import (
    ComplianceConfigSerializer,
    ComplianceConfigListSerializer,
    ComplianceConfigDetailSerializer,
)

from .data import (
    ComplianceDataSerializer,
    ComplianceDataListSerializer,
    ComplianceDataDetailSerializer,
)

from .logs import (
    ComplianceLogSerializer,
    ComplianceLogListSerializer,
    ComplianceLogDetailSerializer,
)

# Serializers adicionales para endpoints específicos
class ComplianceSummarySerializer(serializers.Serializer):
    """Serializer para resumen de cumplimiento"""
    
    total_sources = serializers.IntegerField()
    active_sources = serializers.IntegerField()
    data_sent_count = serializers.IntegerField()
    success_rate = serializers.FloatField()


class ComplianceDataSummarySerializer(serializers.Serializer):
    """Serializer para resumen de datos de cumplimiento"""
    
    total_data = serializers.IntegerField()
    sent_data = serializers.IntegerField()
    confirmed_data = serializers.IntegerField()
    rejected_data = serializers.IntegerField()

__all__ = [
    # Sources
    'ComplianceSourceSerializer',
    'ComplianceSourceListSerializer',
    'ComplianceSourceDetailSerializer',
    
    # Configs
    'ComplianceConfigSerializer',
    'ComplianceConfigListSerializer',
    'ComplianceConfigDetailSerializer',
    
    # Data
    'ComplianceDataSerializer',
    'ComplianceDataListSerializer',
    'ComplianceDataDetailSerializer',
    
    # Logs
    'ComplianceLogSerializer',
    'ComplianceLogListSerializer',
    'ComplianceLogDetailSerializer',
    
    # Summary
    'ComplianceSummarySerializer',
    'ComplianceDataSummarySerializer',
]
