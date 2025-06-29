"""URls Core"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse

# Cambia a tu título personalizado
admin.site.site_header = "Control Telemetria"
admin.site.site_title = "Control Telemetria"  # Cambia a tu título personalizado
admin.site.index_title = "Control Telemetria"

def health_check(request):
    """Health check endpoint for monitoring."""
    return HttpResponse("healthy", content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('api.core.router', 'api'), namespace='api')),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('health/', health_check, name='health_check'),
    path('users/', include('api.apps.users.urls', namespace='users')),
    path('erp/', include('api.apps.erp.urls', namespace='erp')),
    path('telemetry/', include('api.apps.telemetry.urls', namespace='telemetry')),
    path('support/', include('api.apps.support.urls', namespace='support')),
    path('notifications/', include('api.apps.notifications.urls', namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
