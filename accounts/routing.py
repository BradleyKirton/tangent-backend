from django.urls import path
from accounts.consumers import BasicHttpConsumer


urlpatterns = [
	path('long-running', BasicHttpConsumer)
]