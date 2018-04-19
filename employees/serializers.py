from rest_framework import serializers
from employees import models as employee_models
from accounts import serializers as account_serializers


class PositionSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='employees:position-detail')
	
	class Meta:
		model = employee_models.Position
		fields = (
			'id',
			'name',
			'level',
			'url'
		)


class PositionHistorySerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='employees:position-history-detail')
	position = PositionSerializer(read_only=True)

	class Meta:
		model = employee_models.PositionHistory
		fields = (
			'id',
    		'position',
    		'date_started',
    		'is_current',
    		'url'
		)


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='employees:profile-detail')
	user = account_serializers.UserSerializer(read_only=True)
	positions = PositionHistorySerializer(many=True, read_only=True)

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
			'positions',
			'url'
		)