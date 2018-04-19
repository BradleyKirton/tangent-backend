from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from employees import views as employee_views
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


# Required if we use include in the project urls
app_name = 'employees'


# Setup a router for the viewsets
router = DefaultRouter()

router.register('profiles', employee_views.ProfileViewSet)
router.register('positions', employee_views.PositionViewSet)
router.register('position_history', employee_views.PositionHistoryViewSet)


# Root API for 
class EmployeeRootView(APIView):
	"""Root view for the employees application to include viewsets and function based views"""
	def get(self, request: Request) -> Response:
		"""Generate and render a dict of application routes

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


employee_root_view = EmployeeRootView.as_view()



urlpatterns = [
	path('', include(router.urls)),
	path('', employee_root_view, name='employee-root')
]