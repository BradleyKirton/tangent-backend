from django.contrib.auth import models as auth_models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='accounts:user-detail')

	class Meta:
		model = auth_models.User
		fields = (
			'id',
			'username',
			'password',
			'email',
			'first_name',
			'last_name',
			'is_active',
			'is_staff',
			'is_superuser',
			'url'
		)

		extra_kwargs = {
			'password': {'write_only': True, 'style': {'input_type': 'password'}},
			'is_active': {'read_only': True}
		}

	def create(self, validated_data: dict) -> auth_models.User:
		"""Create the user instance

		Args:
		    validated_data: The validated serializer data

		Returns:
		    A django auth user instance
		"""
		# Pop the password so we can set it later
		password = validated_data.pop('password')
		
		# Create a user instance
		user_instance = auth_models.User(**validated_data)
		user_instance.set_password(password)
		user_instance.save()
		
		return user_instance

	def update(self, instance: auth_models.User, validated_data: dict) -> auth_models.User:
		"""Update the user instance

		Args:
		    instance: The user instance to be updated
		    validated_data: The validated serializer data

		Returns:
		    A django auth user instance
		"""
		password = validated_data.pop('password', None)
		
		if password is not None:
			instance.set_password(password)

		for field, value in validated_data.items():
			setattr(instance, field, value)

		instance.save()
		return instance


class GroupSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='accounts:group-detail')

	class Meta:
		model = auth_models.Group
		fields = (
			'id',
			'name',
			'url'
		)