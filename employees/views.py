from rest_framework import serializers
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django_filters import rest_framework as django_filter_backends
from employees import models as employee_models
from employees import serializers as employee_serializers


class ProfileViewSet(
	viewsets.GenericViewSet,
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin):
	"""List, retrieve, update and destroy viewset for employee profiles.

	Profiles are never explicitly created as they will be automatically created
	on the creation of the user instance.
	"""
	queryset = employee_models.Profile.objects.all()
	serializer_class = employee_serializers.ProfileSerializer

	@detail_route(
		methods=('POST', ),
		url_path='add-position',
		serializer_class=employee_serializers.PositionSerializer
	)
	def add_position(self, request: Request, pk: int=None) -> Response:
		name = request.data.get('name', None)
		level = request.data.get('level', None)

		try:
			position = employee_models.Position.objects.get(name=name, level=level)
		except employee_models.Position.DoesNotExist:
			raise serializers.ValidationError(f"The position {name}, {level} does not exist")
		
		# Add the position and respond
		profile = self.get_object()
		employee_models.PositionHistory.objects.create(profile=profile, position=position)

		serializer = employee_serializers.ProfileSerializer(profile, context={'request': request})
		
		return Response(serializer.data)

class PositionViewSet(viewsets.ModelViewSet):
	"""Simple viewset for the position types"""
	queryset = employee_models.Position.objects.all()
	serializer_class = employee_serializers.PositionSerializer


class PositionHistoryViewSet(
	viewsets.GenericViewSet,
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin):
	"""List, retrieve and detroy viewset for position history.
	
	To create a position for an employee use the add position resource on the profile resource.
	"""
	queryset = employee_models.PositionHistory.objects.all()
	serializer_class = employee_serializers.PositionHistorySerializer
	filter_backends = (django_filter_backends.DjangoFilterBackend, )
	filter_fields = ('profile__user__username', )

	@detail_route(
		methods=('POST', ),
		url_path='add-review',
		serializer_class=employee_serializers.ReviewSerializer
	)
	def add_review(self, request: Request, pk: int=None) -> Response:
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		position_history_instance = self.get_object()
		review = serializer.save()
		position_history_instance.reviews.add(review)
		serializer = employee_serializers.PositionHistorySerializer(position_history_instance, context={'request': request})
		
		return Response(serializer.data)


class ReviewViewSet(
	viewsets.GenericViewSet,
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin):
	"""List, retrieve and detroy viewset for reviews.
	
	To create a review use the add-review resource on the position history resource.
	"""
	queryset = employee_models.Review.objects.all()
	serializer_class = employee_serializers.ReviewSerializer