# Django Fundamentals

- [Django Fundamentals](#django-fundamentals)
	- [Setup](#setup)
	- [Django Project Structure: Urls and Views](#django-project-structure-urls-and-views)
	- [Template Basics](#template-basics)
		- [Templates: Inheritance](#templates-inheritance)

## Setup

```bash

### ~Desktop
mkdir <project_name>
cd <project_name>
### ~Desktop/<project_name>
pipenv install django
### activate venv
pipenv shell
### create django project
django-admin startproject <project_name>. # . means current directory
### start development server
python manage.py runserver
# Starting development server at http://127.0.0.1:8000/
### create App
python manage.py startapp <app_name>
```

## Django Project Structure: Urls and Views

<div align="center">
<img src="img/Django_intro.jpg" alt="intro.jpg" width="1000px">
</div>

## Template Basics

<div align="center">
<img src="img/Django_templates.jpg" alt="intro.jpg" width="1000px">
</div>

### Templates: Inheritance

<div align="center">
<img src="img/Django_templates_inheritance.jpg" alt="intro.jpg" width="1000px">
</div>