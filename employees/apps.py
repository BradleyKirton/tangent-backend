from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    name = 'employees'

    def ready(self) -> None:
    	import employees.signals