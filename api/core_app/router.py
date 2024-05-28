"""Urls Customers."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from api.core_app.views import users as views_users
from api.core_app.views import client_profile as views_clientp
from api.core_app.views import interaction_detail as views_detail

router = DefaultRouter()

# Actions
router.register(r'users', views_users.UserViewSet, basename='users')
router.register(r'client_profile',
                views_clientp.ClientProfileViewSet, basename='client_profile')
router.register(r'history_data',
                views_clientp.DataHistoryFactViewSet, basename='history_data')
router.register(r'interaction_detail', views_detail.InteractionXLS)
router.register(r'interaction_detail_json',
                views_detail.InteractionDetailViewSet, basename='interaction_detail_json')


urlpatterns = [
    path('', include(router.urls))
]
