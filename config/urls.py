from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework.documentation import include_docs_urls


# API documentation views
doc_views = include_docs_urls(
	settings.PROJECT_NAME,
	authentication_classes=[],
	permission_classes=[]
)


urlpatterns = [
    path('', doc_views),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]
