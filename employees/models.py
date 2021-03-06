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
        related_name='profile', 
        null=True
    )
    
    phone_number = models.CharField(max_length=10, null=True)
    github_user = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    date_started = models.DateField(auto_now_add=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_TYPES, null=True)
    about_me = models.TextField(null=True)
    race = models.CharField(max_length=1, choices=RACE_TYPES, null=True)
    picture_uri = models.CharField(max_length=255, null=True)
    positions = models.ManyToManyField(Position, through='PositionHistory')

    @property
    def age(self) -> int:
        """Computes the age given the birth_day field"""
        if self.birth_date is None:
            return

        return self._calculate_age(
            self.birth_date,
            datetime.date.today()
        )

    @property
    def years_worked(self) -> int:
        """Computes the years worked"""
        if self.date_started is None:
            return

        return self._calculate_age(
            self.date_started,
            datetime.date.today()
        )

    @property
    def days_to_birthday(self) -> int:
        """Computes the number of days to the instance's birthday"""
        if self.birth_date is None:
            return

        return self._calculate_days_to_birthday(
            self.birth_date, 
            datetime.date.today()
        )

    @staticmethod
    def _calculate_age(birthday, today) -> int:
        """Calculates the employee's age in years given their birthday
        and a value of today.

        Args:
            birthday: A birth date
            current_date: A date to compare the birth date to

        Returns:
            The number of years
        """
        years = today.year - birthday.year
        if today.month == birthday.month and today.day < birthday.day:
            years -= 1
        elif today.month < birthday.month:
            years -= 1
        
        return years

    @staticmethod
    def _calculate_years_worked(date_started, today) -> int:
        """Calculates the number of years an employee has
        worked given the date they starting working
        and a value of today.

        If the date started is future dated, the function will return None

        Args:
            date_started: The date the employee started
            current_date: A date to compare the date started to

        Returns:
            The number of years
        """
        years = (today - date_started).days // 365

        if years < 0:
            return

        return years

    @staticmethod
    def _calculate_days_to_birthday(birthday, today) -> int:
        """Calculates the number of days between the specified birthday
        and the current_date. Both inputs are specifiable by the user and
        the number of days are for the current or next year.

        Args:
            birthday: A birth date
            current_date: A date to compare the birth date to

        Returns:
            The number of days
        """
        if birthday.month == today.month:
            if birthday.day < today.day:
                next_birthday = birthday.replace(year=today.year + 1)
            else:
                next_birthday = birthday.replace(year=today.year)

        elif birthday.month < today.month:
            next_birthday = birthday.replace(year=today.year + 1)
        else:
            next_birthday = birthday.replace(year=today.year)

        return (next_birthday - today).days

    def __str__(self) -> str:
        if self.user is not None:
            return f"{self.user.username}"

        return f"{self.__class__}"


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

    review_date = models.DateField(default=datetime.date.today)
    salary = models.FloatField(null=False)
    review_type = models.CharField(max_length=1, null=False, choices=REVIEW_TYPES)

    def __str__(self) -> str:
        return f"{self.review_date}"


class PositionHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    reviews = models.ManyToManyField(Review, related_name='positions')
    date_started = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.profile.user.username} {self.position.name}"

    @property
    def is_current(self) -> bool:
        """We define the current position as the most recent database entry
        for the user. This is a simple mechanism and could be enhanced with proper versioning
        """
        positions = (PositionHistory
                        .objects
                        .filter(profile=self.profile)
                        .order_by('-id')
                    )
        
        return self == positions.first()