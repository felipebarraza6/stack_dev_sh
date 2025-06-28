"""
Views for the Telemetry Management API.
"""
from rest_framework import viewsets, permissions
from .models.points import CatchmentPoint, InteractionDetail
from .models.schemes import Scheme, Variable
from .serializers import (
    CatchmentPointSerializer,
    SchemeSerializer,
    VariableSerializer,
    InteractionDetailSerializer,
)

class CatchmentPointViewSet(viewsets.ModelViewSet):
    """API endpoint for managing Catchment Points."""
    queryset = CatchmentPoint.objects.all()
    serializer_class = CatchmentPointSerializer
    permission_classes = [permissions.IsAdminUser]

class SchemeViewSet(viewsets.ModelViewSet):
    """API endpoint for managing Schemes."""
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer
    permission_classes = [permissions.IsAdminUser]

class VariableViewSet(viewsets.ModelViewSet):
    """API endpoint for managing Variables."""
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer
    permission_classes = [permissions.IsAdminUser]

class InteractionDetailViewSet(viewsets.ModelViewSet):
    """API endpoint for viewing Interaction Details."""
    queryset = InteractionDetail.objects.all().order_by('-created_at')
    serializer_class = InteractionDetailSerializer
    # Generally, interaction details are read-only for safety.
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'head', 'options'] 