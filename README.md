# Tangent Backend Assignment

The Tangent Backend Assignment is a DRF based backend service.

## Installation
```bash
git clone https://github.com/BradleyKirton/tangent-backend
cd tangent-backend
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```


## TODO
- Accounts
  - Add permission filters
- Employees
  - Add permission filters
  - Build out additional models, serializers and views
  - Build test suites
- Generate application fixtures
- Check what else I am missing