from django.contrib.auth import models as auth_models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = auth_models.User
		fields = (
			'id',
			'username',
			'email',
			'first_name',
			'last_name',
			'is_active',
			'is_staff'
		)


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = auth_models.Group
		fields = (
			'id',
			'name'
		)