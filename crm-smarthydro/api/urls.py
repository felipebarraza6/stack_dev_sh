from django.contrib import admin
from django.urls import path, include
from api.crm import views
from django.conf.urls import url
from django.conf import settings

urlpatterns = [

    path('admin/', admin.site.urls),                    
    path('api/', include(('api.crm.router', 'api'), namespace='api')),

] 
