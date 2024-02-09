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
# router.register(r"", UserMobileLoginViewSet, basename="phone_number_login"),
# router.register(r"", UserVerificationViewSet, basename="verification"),
# router.register(r"", RegenerateTokenViewSet, basename="regenerate_otp"),
router.register(r"", VerificationViewSet, basename="verify"),
# router.register(r"", RegenerateExpiredOTPViewSet, basename="regenerate_otp")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("categories/", CategoriesListAPIView.as_view(), name="categories"),
    path("skills/<int:category_id>/", SkillsListAPIView.as_view(), name="skills"),
    # path(
    #     "user_accessToken/<int:pk>/",
    #     GetUserAccessTokenAPIView.as_view(),
    #     name="user_access_token",
    # ),
    path('locations/', GetLocationsAPiView.as_view(), name="locations"),
    path("users/", GetAllUsersAPIView.as_view(), name="users"),
    path("regenerate_otp/", RegenerateExpiredOTPAPIView.as_view(), name="regenerate_otp")
]
