from django.urls import path
from django.urls import include
from accounts import views as accounts_views
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views as authtoken_views
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


# Required if we use include in the project urls
app_name = 'accounts'


# Setup a router for the viewsets
router = SimpleRouter()
router.register('users', accounts_views.UserViewSet)


class AccountRootView(APIView):
	"""Root view for the accounts application to include viewsets and function based views"""
	def get(self, request: Request) -> Response:
		"""Generate and render a dict of application routes

		Args:
		    request: A DRF request object

		Returns:
		    A DRF response object
		"""
		routes = {
			'users': reverse('accounts:user-list', request=request),
			'obtain-auth-token': reverse('accounts:obtain-auth-token', request=request)
		}

		return Response(routes)


accounts_root_view = AccountRootView.as_view()

# Define the url patterns
urlpatterns = [
	path('', accounts_root_view, name='account-root'),
	path('', include(router.urls)),
	path('obtain-auth-token', authtoken_views.obtain_auth_token, name='obtain-auth-token')
]