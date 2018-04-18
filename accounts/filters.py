from rest_framework import filters


class IsUserOrAdminFilter(filters.BaseFilterBackend):
	"""A custom filter for the user viewset which filters on the current user
	or applies no filter if the user has admin rights"""

	def filter_queryset(self, request, queryset, view):
		if request.user.is_superuser:
			return queryset

		return queryset.filter(pk=request.user.pk)