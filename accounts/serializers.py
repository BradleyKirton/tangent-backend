from django.contrib.auth import models as auth_models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='accounts:user-detail')

	class Meta:
		model = auth_models.User
		fields = (
			'id',
			'username',
			'email',
			'first_name',
			'last_name',
			'is_active',
			'is_staff',
			'is_superuser',
			'url'
		)

		read_only_fields = ('is_active', )


class GroupSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='accounts:group-detail')

	class Meta:
		model = auth_models.Group
		fields = (
			'id',
			'name',
			'url'
		)