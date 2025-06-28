"""
URL patterns for the Telemetry Management API.
"""
from rest_framework.routers import DefaultRouter
from .views import (
    CatchmentPointViewSet,
    SchemeViewSet,
    VariableViewSet,
    InteractionDetailViewSet,
)

router = DefaultRouter()
router.register(r'catchment-points', CatchmentPointViewSet)
router.register(r'schemes', SchemeViewSet)
router.register(r'variables', VariableViewSet)
router.register(r'interaction-details', InteractionDetailViewSet)

urlpatterns = router.urls 