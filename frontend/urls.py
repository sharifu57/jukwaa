from django.urls import path, re_path
from .views import FrontendAppView

urlpatterns = [
    # Your other URL patterns here...
    re_path(r'^.*$', FrontendAppView.as_view(), name='app'),
]
