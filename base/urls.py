from django.urls import path, include
from . import views
from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter
from base.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"", UserRegisterViewSet, basename="register"),
router.register(r"", UserLoginViewSet, basename="login"),
router.register(r"", UserVerificationViewSet, basename="verification"),
router.register(r"", RegenerateTokenViewSet, basename="regenerate_otp")

urlpatterns = [
    path("", include(router.urls)),
]