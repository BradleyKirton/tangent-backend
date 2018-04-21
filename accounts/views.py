from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import models as auth_models
from accounts import serializers as account_serializers
from accounts import permissions as account_permissions
from accounts import filters as account_filters


class UserViewSet(viewsets.ModelViewSet):
	"""This view presents lists of users. The view is read only for non admin users"""
	queryset = auth_models.User.objects.all()
	serializer_class = account_serializers.UserSerializer
	permission_classes = (account_permissions.IsAdminUserOrReadOnly, )
	filter_backends = (account_filters.IsUserOrAdminFilter, )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
	"""This view presents lists of groups. The view is not accessible for non admin users"""
	queryset = auth_models.Group.objects.all()
	serializer_class = account_serializers.GroupSerializer
	permission_classes = (permissions.IsAdminUser, )