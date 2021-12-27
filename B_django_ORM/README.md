# Django ORM

- [Django ORM](#django-orm)
  - [ORM-Models](#orm-models)
    - [default migrations with sqlite3](#default-migrations-with-sqlite3)
    - [Create a new model](#create-a-new-model)
    - [Install PostgreSQL](#install-postgresql)
  - [Relationships](#relationships)
    - [One-to-Many](#one-to-many)
    - [Many-to-Many](#many-to-many)

## ORM-Models

<div align="center">
<img src="img/Django-ORM.jpg" alt="Django-ORM.jpg" width="1000px">
</div>


- [Models](https://docs.djangoproject.com/en/4.0/topics/db/models/#)
- [field-types](https://docs.djangoproject.com/en/4.0/topics/db/models/#field-types)
- [field-types-choices](https://docs.djangoproject.com/en/4.0/topics/db/models/#field-types-choices)

### default migrations with sqlite3

VSCode extension for sqlite3

Name: SQLite Viewer
Publisher: Florian Klampfer
VS [Marketplace Link](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer)

Migrate:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Create a new model

1. register app

```python
INSTALLED_APPS = [
    '...',
    'app',
]
```

2. define model

`app/models.py`

```python
from django.db import models
import uuid

# Create your models here.
class Product(models.Model):
    """
    Product model
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

3. Make migrations and migrate

```bash
python manage.py makemigrations
python manage.py migrate
# shows only sql
python manage.py sqlmigrate app_name migration_file_number
# ex:
python manage.py sqlmigrate app 0001_initial
```

4. register Model for Admin site

`app/model.py`

```python
from django.contrib import admin
# Register your models here.
from .models import Project
# from app.models import Product
admin.site.register(Project)
```

### Install PostgreSQL

[https://www.geeksforgeeks.org/how-to-use-postgresql-database-in-django/](https://www.geeksforgeeks.org/how-to-use-postgresql-database-in-django/)

To get Python working with Postgres, you will need to install the “psycopg2” module.

```bash
pip install psycopg2
```

open the `settings.py` file

now change database settings with this template code

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',
        'USER': 'postgres',
        'PASSWORD': 'pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Run these commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

To show the list of tables with the corresponding schema name in PgSql, run this statement:

```sql
SELECT * FROM information_schema.tables where table_schema = 'public';
```

## Relationships

### One-to-Many

<div align="center">
<img src="img/1-m.jpg" alt="OneToMany.jpg" width="1000px">
</div>

```python
from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# One `Product` can have Many `Reviews`
# One `Review` can only belong to one `Product`

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # above line will create 'product_id' column in Review table

    VOTE_CHOICES = (
        ('up', 'UP VOTE'),
        ('down', 'DOWN VOTE'),
    )
    body = models.TextField(null=True, blank=True)
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES, default='up')
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          unique=True, primary_key=True)

    def __str__(self):
        return self.body[:20]
```

Update `admin.py`:


```python
from django.contrib import admin
# Register your models here.
from .models import Product, Review
# from app.models import Product, Review
admin.site.register(Product)
admin.site.register(Review)
# ....

```


### Many-to-Many

<div align="center">
<img src="img/Django-ORM-Relationship-M-M.jpg" alt="Django-ORM-Relationship-M-M.jpg" width="1000px">
</div>

```python
from django.db import models
import uuid
# M to M: Product to Tag

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField('Tags', blank=True, related_name='tags')
    # 1. Tags` instead of Tag because Tag Model is defined later
    # 2. related_name='tags' is used to avoid naming convention
    #    when we access the tags from Product model
    #    i.e. instead of product.tags_set.all(),we can use product.tags.all()
    #       p = Product.objects.first()
    #       p.tags.all()

    def __str__(self):
        return self.title

class Tags(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          primary_key=True, unique=True)

    products = models.ManyToManyField(
        Product, blank=True, related_name='products')
    # Many to Many relation can be defined in just either one of the models.
    # Or both of them for better admin interface.
    # t = Tags.objects.first()
    # t.products.all()

    def __str__(self):
        return self.name
```

Update `admin.py`:

```python
from django.contrib import admin

# Register your models here.
from .models import Product, Tags
# from app.models import Product, Tags
admin.site.register(Product)
admin.site.register(Tags)
# ....

```