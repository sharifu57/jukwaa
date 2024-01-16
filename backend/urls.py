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
    path("create_project/", PostProjectAPIView.as_view(), name="create_project"),
    path("budgets/", BudgetListAPIView.as_view(), name="budgets"),
    path(
        "get_match_projects/<int:category_id>/",
        GetMatchProjectsAPIView.as_view(),
        name="get_match_projects",
    ),
    path(
        "get_user_projects/<int:user_id>/",
        GetProjectsByUserIdAPIView.as_view(),
        name="get_user_projects",
    ),
    path("view_project/<int:pk>/",
         ViewOneProjectAPIView.as_view(), name="view_project"),
    path(
        "create_new_bid/",
        CreateBidAPIView.as_view(),
        name="create_new_bid"
    ),
    path(
        "project_bidders/<int:project_id>/",
        ProjectBiddersAPIView.as_view(),
        name="project_bidders"
    ),
    path(
        "category_projects/",
        GetProjectsByCategoryAPIView.as_view(),
        name="category_projects"
    ),
    path(
        "projects/",
        GetAllProjectsAPiView.as_view(),
        name="projects"
    )
]
