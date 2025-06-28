from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, FieldVisitViewSet

app_name = 'support'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'visits', FieldVisitViewSet, basename='visit')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
] 