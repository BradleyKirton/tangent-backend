from rest_framework import viewsets
from employees import models as employee_models
from employees import serializers as employee_serializers


class ProfileViewSet(viewsets.ModelViewSet):
	queryset = employee_models.Profile.objects.all()
	serializer_class = employee_serializers.ProfileSerializer


class PositionViewSet(viewsets.ModelViewSet):
	queryset = employee_models.Position.objects.all()
	serializer_class = employee_serializers.PositionSerializer


class PositionHistoryViewSet(viewsets.ModelViewSet):
	queryset = employee_models.PositionHistory.objects.all()
	serializer_class = employee_serializers.PositionHistorySerializer