"""
URLs para Desarrollo Local
Incluye documentación automática con Swagger/OpenAPI
"""
from django.urls import path, include
from django.contrib import admin
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# URLs de documentación automática
urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # Documentación automática
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Base (Servicio Interno)
    path('api/base/', include('api.config.urls.base')),
    
    # API Frontend (Capa Externa)
    path('api/frontend/', include('api.config.urls.frontend')),
    
    # URLs de autenticación
    path('api/auth/', include('rest_framework.urls')),
    
    # URLs de usuarios
    path('api/users/', include('api.apps.users.views.router')),
    
    # URLs de providers
    path('api/providers/', include('api.apps.providers.router')),
    
    # URLs de variables
    path('api/variables/', include('api.apps.variables.router')),
    
    # URLs de catchment
    path('api/catchment/', include('api.apps.catchment.router')),
    
    # URLs de compliance
    path('api/compliance/', include('api.apps.compliance.router')),
    
    # URLs de telemetría
    path('api/telemetry/', include('api.apps.telemetry.router')),
] 