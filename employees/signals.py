from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import models as auth_models
from employees import models as employee_models


@receiver(signals.post_save, sender=auth_models.User)
def post_user_save(sender: object, instance: auth_models.User, created: bool, **kwargs) -> None:
	"""The employee instance is automatically created on the creation of the user instance

	Args:
	    sender: The user model class
	    instance: An instance of the user model
	    created: A boolean, true if the instance was created
	"""
	if not created:
		return

	employee_models.EmployeeProfile.objects.create(user=instance)