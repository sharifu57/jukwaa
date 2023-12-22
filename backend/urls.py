from django.urls import path, include
from . import views
from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter
from backend.views import *


router = DefaultRouter()
# router.register(r"", UserRegisterViewSet, basename="register"),

urlpatterns = [
    path("", include(router.urls)),
    path("statistics/", ProjectStatisticsAPIView.as_view(), name="statistics"),
]
