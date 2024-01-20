# Django + TailwindCSS + HTMX


## Setup

- [https://www.geeksforgeeks.org/how-to-use-tailwind-css-with-django/](https://www.geeksforgeeks.org/how-to-use-tailwind-css-with-django/)
- [https://testdriven.io/blog/django-htmx-tailwind/](https://testdriven.io/blog/django-htmx-tailwind/)
- [https://flowbite.com/docs/getting-started/django/](https://flowbite.com/docs/getting-started/django/)

```bash
pnpm init
pnpm install -D tailwindcss
npx tailwindcss init
mkdir .venv
pipenv install django django-compressor django-browser-reload django-extensions ipython bpython
pipenv shell
# using venv...
# python -m venv .venv
# .\.venv\Scripts\activate
```

```bash
django-admin startproject core .
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Tailwindcss

Requirements:`Django Compressor`

Django Compressor is an extension designed for managing (compressing/caching) static assets in a Django application. With it, you create a simple asset pipeline for:

- Combining and minifying multiple CSS and JavaScript files down to a single file for each
- Creating asset bundles for use in your templates


1. Add `compressor` to the installed apps inside the `settings.py` file:


```python
# config/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',  # new
]
```

2. Configure the `compressor` inside the `settings.py` file:


```python
# default / The list of finder backends that know how to find static files in various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# django-compressor
COMPRESS_ROOT = BASE_DIR / "static"
COMPRESS_ENABLED = True
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

```

3. Enable root-level templates :create a new `templates/` directory inside the project folder and update `settings.py` folder:

```python
# config/settings.py
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'], # new
        ...
    },
]
```

4. Create two new folders and an `input.css` file inside the `static/src/` folder:

```css
/* static/src/input.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```


5. Update `tailwind.config.js` like so:


```typescript
/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		// Templates within theme app (e.g. base.html)
		'./templates/**/*.html',
		// Templates in other apps
		'./../templates/**/*.html'
		// // Include JavaScript files that might contain Tailwind CSS classes
		// '../../**/*.js',
		// // Include Python files that might contain Tailwind CSS classes
		// '../../**/*.py'
	],
	theme: {
		extend: {}
	},
	plugins: []
};
```

6. Run the following command to watch for changes and compile the Tailwind CSS code:

```json
"scripts": {
	"dev:css": "tailwindcss -i ./static/src/input.css -o ./static/src/output.css --minify --watch"
},
```

7. Load precessed `output.css` in `templates\_base.html`

`templates\_base.html`

```html
{% load compress %} {% load static %}
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>{% block page_title %}Django + Tailwind CSS + HTMX{% endblock page_title %}</title>
		{% compress css %}
		<link rel="stylesheet" href="{% static 'src/output.css' %}" />
		<!-- HTMX start -->
		{% endcompress %}
	</head>
	<body>
		{% block content %} {% endblock content %}
	</body>
</html>
```


### HTMX

1. Download `https://unpkg.com/htmx.org@1.9.10/dist/htmx.js` and save to `static/src`
2. Load `htmx.js` in `_base.html` also set header to use crf_token


`templates\_base.html`

```html
{% load compress %} {% load static %}
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>{% block page_title %}Django + Tailwind CSS + HTMX{% endblock page_title %}</title>
		{% compress css %}
		<link rel="stylesheet" href="{% static 'src/output.css' %}" />
		{% endcompress %}
		<!-- HTMX start -->
		{% compress js %}
		<script type="text/javascript" src="{% static 'src/htmx.js' %}"></script>
		{% endcompress %}
		<!-- HTMX end-->
	</head>
	<body>
		{% block content %} {% endblock content %}
		<!-- HTMX start -->

		<script>
			document.body.addEventListener('htmx:configRequest', (event) => {
				event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
			});
		</script>
		<!-- HTMX end-->
	</body>
</html>
```

