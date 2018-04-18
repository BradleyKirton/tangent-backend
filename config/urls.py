from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework.documentation import include_docs_urls
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


# API documentation views
doc_views = include_docs_urls(
	settings.PROJECT_NAME,
	authentication_classes=[],
	permission_classes=[]
)


# Root API for 
class RootView(APIView):
	"""Root view for the project"""
	def get(self, request: Request) -> Response:
		"""Generate and render a dict of application root views

		Args:
		    request: A DRF request object

		Returns:
		    A DRF response object
		"""
		routes = {
			'accounts': reverse('accounts:account-root', request=request),
			'employees': reverse('employees:employee-root', request=request),
		}

		return Response(routes)


root_view = RootView.as_view()


urlpatterns = [
    path('', doc_views),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', root_view),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/employees/', include('employees.urls', namespace='employees')),
]