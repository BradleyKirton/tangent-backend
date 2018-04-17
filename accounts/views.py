from rest_framework import viewsets
from django.contrib.auth import models as auth_models
from accounts import serializers as account_serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = auth_models.User.objects.all()
	serializer_class = account_serializers.UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = auth_models.Group.objects.all()
	serializer_class = account_serializers.GroupSerializer