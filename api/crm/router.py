"""Urls Customers."""

# Django
from django.urls import include,path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from api.crm.views import supports as views_supports
from api.crm.views import actions as views_actions
from api.crm.views import clients as views_clients
from api.crm.views import employess as views_employess
from api.crm.views import users as views_users
from api.crm.views import client_profile as views_clientp
from api.crm.views import quotation as views_quotations 
from api.crm.views import interaction_detail as views_detail
from api.crm.views import webinars as views_webinars
from api.crm.views import profile_footprints as views_footprints

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
router.register(r'wells', views_quotations.WellsViewSet, basename=
        'wells')
router.register(r'interaction_detail', views_detail.InteractionXLS)
router.register(r'interaction_detail_json', views_detail.InteractionDetailViewSet, basename= 'interaction_detail_json')
router.register(r'webinars', views_webinars.WebinarsViewSet, basename= 'webinars')
router.register(r'profile_footprints', views_footprints.ProfileFootprintsViewSet, basename= 'profile_footprints')
router.register(r'clients_external', views_clients.ClientExternalViewSet, basename='clients_external')
router.register(r'support_sections', views_supports.SupportSectionViewSet, basename='support_sections')
router.register(r'support_tickets', views_supports.TicketSupportViewSet, basename='support_ticket')
router.register(r'ticket_answers', views_supports.AnswerTicketViewSet, basename='ticket_answer')
router.register(r'fields', views_footprints.FieldSectionViewSet, basename='fields')


urlpatterns = [
    path('', include(router.urls))
]
