from django.contrib import admin
from employees.models import Profile
from employees.models import Position
from employees.models import PositionHistory
from employees.models import Review


# Register the models on the admin site
admin.site.register(Profile)
admin.site.register(Position)
admin.site.register(PositionHistory)
admin.site.register(Review)