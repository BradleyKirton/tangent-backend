from rest_framework import serializers
from employees import models as employee_models
from accounts import serializers as account_serializers


class PositionSerializer(serializers.ModelSerializer):
	class Meta:
		model = employee_models.Position
		fields = (
			'id',
			'name',
			'level',
			'market_salary'
		)


class PositionHistorySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = employee_models.PositionHistory
		fields = (
			'id',
    		'employee',
    		'position',
    		'date_started'
		)


class ProfileSerializer(serializers.ModelSerializer):
	user = account_serializers.UserSerializer(read_only=True)
	positions = PositionSerializer(many=True)

	class Meta:
		model = employee_models.Profile
		fields = (
			'id',
			'user',
			'phone_number',
			'email',
			'github_user',
			'birth_date',
			'date_started',
			'gender',
			'race',
			'age',
			'years_worked',
			'days_to_birthday',
			'positions'
		)