"""
Main URL router for the ERP application.

This file aggregates routers from all the feature modules within the ERP app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .projects.views import ClientViewSet, ProjectViewSet
# from .invoicing.views import InvoiceViewSet  # Uncomment when InvoiceViewSet is created

# Main router for the entire ERP app
router = DefaultRouter()

# Register routes from the 'projects' module
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'projects', ProjectViewSet, basename='project')

# Register routes from the 'invoicing' module
# router.register(r'invoices', InvoiceViewSet, basename='invoice') # Uncomment when ready

urlpatterns = [
    # Main ERP routes
    path('', include(router.urls)),
    
    # Include sub-module routes
    path('quotations/', include('api.apps.erp.quotations.urls')),
    path('payments/', include('api.apps.erp.payments.urls')),
    path('banking/', include('api.apps.erp.banking.urls')),
] 