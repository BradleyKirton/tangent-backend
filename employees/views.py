from rest_framework import viewsets
from employees import models as employee_models
from employees import serializers as employee_serializers


class EmployeeProfileViewSet(viewsets.ModelViewSet):
	queryset = employee_models.EmployeeProfile.objects.all()
	serializer_class = employee_serializers.EmployeeProfileSerializer