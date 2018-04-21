from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
	"""Custom permission class for the accounts application.
	
	The view provides read only access for non admin users and
	all users must be authenticated
	"""
	def has_permission(self, request, view) -> bool:
		"""Checks that the user is authenticated, if so admin users are
		given full permissions while non admin users are given read only access


		Args:
		    request: A DRF request object
		    view: The calling view

		Returns:
		    A boolean which determines the users permission on a particular view
		"""
		if not request.user.is_authenticated:
			return False

		if request.user.is_superuser:
			return True

		return request.method in permissions.SAFE_METHODS
