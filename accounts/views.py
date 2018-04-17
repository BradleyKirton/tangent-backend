from rest_framework import viewsets
from django.contrib.auth import models as auth_models
from accounts import serializers as accounts_serializers



class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = auth_models.User.objects.all()
	serializer_class = accounts_serializers.UserSerializer