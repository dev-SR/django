# All thing Django Setups

- [All thing Django Setups](#all-thing-django-setups)
  - [Setup Templates](#setup-templates)
  - [django-debug-toolbar](#django-debug-toolbar)
    - [Setup](#setup)
  - [django-browser-reload](#django-browser-reload)
  - [django-extensions](#django-extensions)
    - [Setup](#setup-1)
    - [admin\_generator](#admin_generator)
    - [RunScript](#runscript)
  - [Faker Lib](#faker-lib)


## Setup Templates

```python

1. Register `templates` dir for placing all htmls
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # <---- Add "templates" dir here
        "APP_DIRS": True,
        # ..
    },
]
```

2. Place your htmls at `templates/app`


## django-debug-toolbar

### Setup 

1. Install the package
```bash
uv add django-debug-toolbar
```

2. Ensure you have `"django.contrib.staticfiles`" in your `INSTALLED_APPS`.
3. Add `debug_toolbar` to your `INSTALLED_APPS` setting:


```python
INSTALLED_APPS = [
    # ...
    "debug_toolbar",
    # ...
]
```

4. Add the Middleware


```python
MIDDLEWARE = [
    # ...
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # ...
]
```

> The order of MIDDLEWARE is important. **You should include the Debug Toolbar middleware as early as possible** in the list (i.e. after `CommonMiddleware`). However, it must come after any other middleware that encodes the response’s content, such as GZipMiddleware.

5. Configure Internal IPs
The Debug Toolbar is shown only if your IP address is listed in Django’s INTERNAL_IPS setting. This means that for local development, you must add "127.0.0.1" to INTERNAL_IPS. You’ll need to create this setting if it doesn’t already exist in your settings module:


```python
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
```

6. Include the app URLs in your root URLconf:  `config\urls.py`


```python
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
```


## django-browser-reload

1. Install 

```bash
uv add django-browser-reload
```

2. settings
3. Add the middleware:


```python
MIDDLEWARE = [
    # ...
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    # ...
]
```


4. Include the app URLs in your root URLconf:
   

```python
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        # ...
        path("__reload__/", include("django_browser_reload.urls")),
    ]
```


## django-extensions

### Setup 

1. Install

```bash
uv add django-extensions
```

### admin_generator

```bash
 python manage.py admin_generator <your_app_name>
# or
uv run manage.py admin_generator <app>
 ```


### RunScript

[https://django-extensions.readthedocs.io/en/latest/runscript.html](https://django-extensions.readthedocs.io/en/latest/runscript.html)


1. To get started create a `scripts/__init__.py` file in your project root, next to `manage.py`
2. Next, create a python file with the name of the script you want to run within the scripts directory (i.e. `scripts/seed_db.py`)

```python
def run():
    print("Seeding....")

```

    
1. To run any script you use the command runscript with the name of the script that you want to run.

```bash
python manage.py runscript seed_db
# or
uv run manage.py runscript seed_db
```



## Faker Lib

```bash
pip install Faker faker_commerce
uv add Faker faker_commerce
```

`scripts\seed.py`

```python
from faker import Faker
import faker_commerce

# https://github.com/nicobritos/python-faker-commerce/blob/main/faker_commerce/__init__.py
import random

def run():
    fake = Faker()
    fake.add_provider(faker_commerce.Provider)
    for _ in range(20):
        title = fake.ecommerce_name()
        price = fake.random_int(min=100, max=1000)
        stats = random.choice(["active", "inactive"])
        tags = fake.random_choices(["new", "just_arrival", "old", "classic"], length=2)
        print(f"{title} price: {price}, status: {stats} tags: {tags}")
```


