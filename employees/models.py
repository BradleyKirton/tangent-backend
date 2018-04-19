import datetime

from django.db import models
from django.contrib.auth import models as auth_models


class Position(models.Model):
    FRONTEND_DEV = ('Front-end Developer', 'Front-end Developer')
    BACKEND_DEV = ('Back-end Developer', 'Back-end Developer')
    PROJECT_MANAGER = ('Project Manager', 'Project Manager')
    
    NAME_TYPES = (
        FRONTEND_DEV,
        BACKEND_DEV,
        PROJECT_MANAGER
    )
    
    JUNIOR = ('Junior', 'Junior')
    SENIOR = ('Senior', 'Senior')

    LEVEL_TYPES = (
        JUNIOR, 
        SENIOR
    )

    name = models.CharField(max_length=10, null=True, choices=NAME_TYPES)
    level = models.CharField(max_length=10, null=True, choices=LEVEL_TYPES)
    market_salary = models.FloatField(null=True)

    class Meta:
        unique_together = (
            ('name', 'level'),
        )

    def __str__(self) -> str:
        return f"{self.name} - {self.level}"


class Profile(models.Model):
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
    positions = models.ManyToManyField(Position, through='PositionHistory')

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

    def __str__(self) -> str:
        return f"{self.user.username}"


class Review(models.Model):
    PERFORMACE_INCREASE = ('P', 'Performance Increase')
    STARTING_SALARY = ('S', 'Starting Salary')
    ANNUAL_INCREASE = ('A', 'Annual Increase')
    EXPECTATION_REVIEW = ('E', 'Expectation Review')

    REVIEW_TYPES = (
        PERFORMACE_INCREASE,
        STARTING_SALARY,
        ANNUAL_INCREASE,
        EXPECTATION_REVIEW
    )

    review_date = models.DateField(auto_now_add=True)
    salary = models.FloatField(null=False)
    review_type = models.CharField(max_length=1, null=False, choices=REVIEW_TYPES)

    def __str__(self) -> str:
        return f"{self.review_date}"


class PositionHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    date_started = models.DateField(auto_now_add=True)
    review = models.ManyToManyField(Review)

    def __str__(self) -> str:
        return f"{self.profile.user.username} {self.position.name}"

    @property
    def is_current(self) -> bool:
        """We define the current position as the most recent database entry
        for the user. This is a simple mechanism and could be enhanced with proper versioning
        """
        positions = (Position
                        .objects
                        .filter(pk=self.pk)
                        .order_by('-id')
                    )
        
        return self == positions.first()