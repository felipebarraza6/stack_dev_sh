from django.contrib import admin
from django.urls import path, include
from api.crm import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),                    
    path('api/', include(('api.crm.router', 'api'), namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
