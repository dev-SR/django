# Customizing the Admin Site

- [Customizing the Admin Site](#customizing-the-admin-site)
	- [default migrations with sqlite3](#default-migrations-with-sqlite3)
	- [Registering Models](#registering-models)

## default migrations with sqlite3

VSCode extension for sqlite3
Name: SQLite Viewer Publisher: [Florian Klampfer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer)

Migrate:

```python
python manage.py migrate
python manage.py createsuperuser
```

Create a new model

register app

```python
INSTALLED_APPS = [
    '...',
    'app',
]
```

## Registering Models

```python
from django.contrib import admin

# Register your models here.
# from .models import Author
# from app.models import Author
# admin.site.register(Author)

from . import models
admin.site.register(models.Product)
admin.site.register(models.Review)
admin.site.register(models.Tag)
admin.site.register(models.Book)
admin.site.register(models.Author)
```
