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
    path('locations/', GetLocationsAPiView.as_view(), name="locations"),
    path("users/", GetAllUsersAPIView.as_view(), name="users"),
    path("regenerate_otp/", RegenerateExpiredOTPAPIView.as_view(), name="regenerate_otp"),
    path("team/", AllTeamAPIView.as_view(), name="team"),
    path("employers_logo/", GetCompaniesLogoAPIView.as_view(), name="employers_logo"),
    path("reset_password/", ResetPasswordAPIView.as_view(), name="reset_password"),
    path("reset_password_confirm/<uidb64>/<token>/", ResetNewPasswordConfirmAPIView.as_view(), name="password_reset_confirm"),
    path('set-new-password/', SetNewPasswordAPIView.as_view(), name='set_new_password'),
    path('experiences/', GetExperienceAPIView.as_view(), name="experiences"),
    path('user_details/<str:user_id>/', GetUserDetailsAPIView.as_view(), name="userDetails"),
    path('update_profile_image/<int:user_id>/', UpdateUserProfileImageAPIView.as_view(), name="profileImage"),
    path('forgot_password/', ForgotPasswordAPIView.as_view(), name="forgot_password")
]
