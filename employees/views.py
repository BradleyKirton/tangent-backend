from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django_filters import rest_framework as django_filter_backends
from employees import models as employee_models
from employees import serializers as employee_serializers


class ProfileViewSet(viewsets.ModelViewSet):
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
	queryset = employee_models.Position.objects.all()
	serializer_class = employee_serializers.PositionSerializer


class PositionHistoryViewSet(viewsets.ModelViewSet):
	queryset = employee_models.PositionHistory.objects.all()
	serializer_class = employee_serializers.PositionHistorySerializer
	filter_backends = (django_filter_backends.DjangoFilterBackend, )
	filter_fields = ('profile__user__username', )


class ReviewViewSet(viewsets.ModelViewSet):
	queryset = employee_models.Review.objects.all()
	serializer_class = employee_serializers.ReviewSerializer


	@detail_route(
		methods=('POST', ),
		url_path='add-review',
	)
	def add_review(self, request: Request, pk: int=None) -> Response:
		return Response({})

