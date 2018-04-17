from rest_framework import serializers
from employees import models as employee_models
from accounts import serializers as account_serializers


class EmployeeProfileSerializer(serializers.ModelSerializer):
	user = account_serializers.UserSerializer(read_only=True)

	class Meta:
		model = employee_models.EmployeeProfile
		fields = (
			'user',
			'phone_number',
			'email',
			'github_user',
			'birth_date',
			'year_started',
			'gender',
			'race',
			'age',
			'years_worked',
			'days_to_birthday'
		)