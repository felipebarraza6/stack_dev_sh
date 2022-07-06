"""Urls Customers."""

# Django
from django.urls import include,path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from api.crm.views import actions as views_actions
from api.crm.views import clients as views_clients
from api.crm.views import employess as views_employess
from api.crm.views import users as views_users
from api.crm.views import client_profile as views_clientp
from api.crm.views import quotation as views_quotations 


router = DefaultRouter()

#Actions

router.register(r'users', views_users.UserViewSet, basename='users')

router.register(r'actions', views_actions.ActionViewSet, basename='actions')
router.register(r'type_actions', views_actions.TypeActionViewSet, basename= 'type_actions')

router.register(r'clients', views_clients.ClientViewSet, basename= 'clients')

router.register(r'employess', views_employess.EmployeeViewSet, basename= 'employess')
router.register(r'client_profile', views_clientp.ClientProfileViewSet, basename= 'client_profile')
router.register(r'history_data', views_clientp.DataHistoryFactViewSet, basename= 'history_data')
router.register(r'quotation', views_quotations.QuotationViewSet, basename=
        'quotation')



urlpatterns = [
    path('', include(router.urls))
]
