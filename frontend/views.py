from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
import os

class FrontendAppView(View):
    def get(self, request):
        try:
            with open(os.path.join(settings.STATIC_ROOT, 'frontend/index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse(
                """
                This URL is only used when you have built the production version of the app. 
                Visit http://localhost:3000/ instead, or run `npm run build` to test the production version.
                """,
                status=501,
            )
