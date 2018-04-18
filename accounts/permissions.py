from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
	"""Custom permission class for the accounts application
	
	The class 
	"""
	def has_permission(self, request, view):
		if not request.user.is_authenticated:
			return False

		if request.user.is_superuser:
			return True

		return request.method in permissions.SAFE_METHODS
