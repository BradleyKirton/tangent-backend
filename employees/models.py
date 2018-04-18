import datetime

from django.db import models
from django.contrib.auth import models as auth_models



class EmployeeProfile(models.Model):
    GENDER_TYPES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    RACE_TYPES = (
        ('B', 'Black African'),
        ('C', 'Coloured'),
        ('I', 'Indian or Asian'),
        ('W', 'White'),
        ('N', 'None Dominant')
    )
    
    user = models.OneToOneField(
        auth_models.User, 
        on_delete=models.SET_NULL, 
        related_name='employee_profile', 
        null=True
    )
    
    phone_number = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)
    github_user = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    date_started = models.DateField(auto_now_add=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_TYPES, null=True)
    race = models.CharField(max_length=1, choices=RACE_TYPES, null=True)
    
    @property
    def age(self) -> int:
        if self.birth_date is None:
            return

        delta = datetime.date.today() - self.birth_date
        return delta.days // 365

    @property
    def years_worked(self) -> int:
        delta = datetime.date.now() - self.date_started
        return delta.days // 365
        

    @property
    def days_to_birthday(self) -> int:
        if self.birth_date is None:
            return

        now = datetime.date.now()
        this_years_bday = self.birth_date.replace(year=now.year)

        if self.birth_date.month < now.month:
            now = now.replace(year=now.year + 1)
        
        delta = now - this_years_bday
        return delta.days