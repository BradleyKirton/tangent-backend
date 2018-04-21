from rest_framework import serializers
from rest_framework.reverse import reverse
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


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='employees:review-detail')
	position = serializers.SlugRelatedField(slug_field='name', source='positions.position', read_only=True)

	class Meta:
		model = employee_models.Review
		fields = (
			'id',
    		'review_date',
    		'salary',
    		'review_type',
    		'position',
			'url'
		)


class PositionHistorySerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='employees:position-history-detail')
	username = serializers.SlugRelatedField(slug_field='username', source='profile.user', read_only=True)
	position = PositionSerializer(read_only=True)
	reviews = ReviewSerializer(many=True, read_only=True)
	add_review = serializers.SerializerMethodField()
	profile = serializers.SerializerMethodField()

	def get_profile(self, instance) -> str:
		"""Returns the full uri for the add review detail route

		Args:
		    instance: A profile instance

		Returns:
		    A URI string
		"""
		return reverse('employees:profile-detail', kwargs={'pk': instance.profile.pk}, request=self.context['request'])

	def get_add_review(self, instance) -> str:
		"""Returns the full uri for the add review detail route

		Args:
		    instance: A profile instance

		Returns:
		    A URI string
		"""
		return reverse('employees:position-history-add-review', kwargs={'pk': instance.pk}, request=self.context['request'])

	class Meta:
		model = employee_models.PositionHistory
		fields = (
			'id',
			'username',
    		'position',
    		'reviews',
    		'date_started',
    		'is_current',
    		'add_review',
    		'profile',
    		'url'
		)

		read_only_fields = ('is_current', )


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='employees:profile-detail')
	user = account_serializers.UserSerializer(read_only=True)
	positions = PositionHistorySerializer(many=True, read_only=True, source='positionhistory_set')
	add_position = serializers.SerializerMethodField()

	def get_add_position(self, instance) -> str:
		"""Returns the full uri for the add position detail route

		Args:
		    instance: A profile instance

		Returns:
		    A URI string
		"""
		return reverse('employees:profile-add-position', kwargs={'pk': instance.pk}, request=self.context['request'])

	class Meta:
		model = employee_models.Profile
		fields = (
			'id',
			'user',
			'phone_number',
			'github_user',
			'birth_date',
			'date_started',
			'gender',
			'race',
			'age',
			'years_worked',
			'days_to_birthday',
			'about_me',
			'positions',
			'add_position',
			'url'
		)