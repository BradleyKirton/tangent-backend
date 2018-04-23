import os
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from employees.models import Profile


ACCOUNTS_FIXTURES_PATH = os.path.join(settings.BASE_DIR, 'accounts/fixtures/accounts.json')
EMPLOYEES_FIXTURES_PATH = os.path.join(settings.BASE_DIR, 'employees/fixtures/employees.json')


class Command(BaseCommand):
    help = 'Loads the django fixtures. This command is only necessary to avoid the post save signal on User.'

    def handle(self, *args, **options):
        self.stdout.write(ACCOUNTS_FIXTURES_PATH)
        self.stdout.write(EMPLOYEES_FIXTURES_PATH)
        
        with open(ACCOUNTS_FIXTURES_PATH) as f:
            accounts = json.load(f)
        
        with open(EMPLOYEES_FIXTURES_PATH) as f:
            employees = json.load(f)