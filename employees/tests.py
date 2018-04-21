import datetime

from django.contrib.auth import models as auth_models
from django.test import TestCase
from employees import models as employee_models


def get_user_and_profile(profile_defaults):
	user, created = auth_models.User.objects.get_or_create(username='test', password='secret')

	# User profile is automatically created with a signal on the user creation
	profile = employee_models.Profile.objects.get(user=user)

	# Update the profile	
	for key, value in profile_defaults.items():
		if hasattr(profile, key):
			setattr(profile, key, value)

	profile.save()

	return user, profile


class ProfileModelTest(TestCase):
	def test_days_to_birthday(self):
		# Test the model property first
		birthday = datetime.date(1986, 2, 18)
		user, profile = get_user_and_profile({'birth_date': birthday})
		
		today = datetime.date.today()

		if birthday.month <= today.month:
			next_birthday = birthday.replace(year=today.year + 1)
		else:
			next_birthday = birthday.replace(year=today.year)
		
		days = (next_birthday - today).days

		self.assertEqual(profile.days_to_birthday, days)

		# The days to birthday is computed by another function in the class
		# The reason for this is to make the code testable, the next tests 
		# test the _calculate_days_to_birthday function for multiple scenarios
		today = datetime.date(1986, 2, 19)
		birthday = datetime.date(1986, 2, 18)

		days = employee_models.Profile._calculate_days_to_birthday(birthday, today)
		self.assertEqual(days, 364)

		today = datetime.date(1986, 2, 17)
		birthday = datetime.date(1986, 2, 18)

		days = employee_models.Profile._calculate_days_to_birthday(birthday, today)
		self.assertEqual(days, 1)

		today = datetime.date(1986, 2, 18)
		birthday = datetime.date(1986, 2, 18)
		
		days = employee_models.Profile._calculate_days_to_birthday(birthday, today)
		self.assertEqual(days, 0)