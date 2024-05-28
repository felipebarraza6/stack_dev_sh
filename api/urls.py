from django.contrib import admin
from django.urls import path, include, re_path
from api.crm import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

admin.site.site_header = "Control Telemetria - Smart Hydro"  # Cambia a tu título personalizado
admin.site.site_title = "Control Telemetria"  # Cambia a tu título personalizado
admin.site.index_title = "Control Telemetria"

urlpatterns = [
    path('admin/', admin.site.urls),                    
    path('api/', include(('api.crm.router', 'api'), namespace='api')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
