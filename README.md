# Django

## Setup

### Crating Virtual Environment with `pipenv`

```bash

### ~Desktop
mkdir django-project
cd django-project

### ~Desktop/django-project
pipenv install django
# Successfully created virtual environment!
# Virtualenv location: C:\Users\X\.virtualenvs\django-project-zqtDNc_4

### activate venv
pipenv shell
# (django-project-zqtDNc_4) ~Desktop/django-project

### create django project
django-admin startproject django-project . # . means current directory

### start development server
python manage.py runserver
# Starting development server at http://127.0.0.1:8000/

### create App
python manage.py startapp app
```