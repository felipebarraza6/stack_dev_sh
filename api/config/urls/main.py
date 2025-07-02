"""URLs Principales del Sistema de Telemetría"""
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


# Configuración del admin
admin.site.site_header = "Control Telemetría"
admin.site.site_title = "Control Telemetría"
admin.site.index_title = "Control Telemetría"

# URLs principales
urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/telemetry/', include('api.apps.telemetry.router')),
    path('api/catchment/', include('api.apps.catchment.router')),
    path('api/users/', include('api.apps.users.router')),
    path('api/variables/', include('api.apps.variables.router')),
    path('api/providers/', include('api.apps.providers.router')),
    path('api/compliance/', include('api.apps.compliance.router')),
    
    # Autenticación y utilidades
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/auth/', include('rest_framework.urls')),
    
    # Archivos estáticos y media
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
