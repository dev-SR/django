# Django + TailwindCSS + HTMX


## Setup

- [https://www.geeksforgeeks.org/how-to-use-tailwind-css-with-django/](https://www.geeksforgeeks.org/how-to-use-tailwind-css-with-django/)
- [https://testdriven.io/blog/django-htmx-tailwind/](https://testdriven.io/blog/django-htmx-tailwind/)
- [https://flowbite.com/docs/getting-started/django/](https://flowbite.com/docs/getting-started/django/)

```bash
# python -m venv .venv
# .\.venv\Scripts\activate
# pip install django django-compressor
mkdir .venv
pipenv install django django-compressor
pipenv shell
django-admin startproject config .
python manage.py startapp todos
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
    'todos',  # new
    'compressor',  # new
]
```

2. Configure the `compressor` inside the `settings.py` file:


```python
# config/settings.py

# django-compressor
COMPRESS_ROOT = BASE_DIR / "static" # defines the absolute location from where the files to be compressed are read from and the compressed files are written to.
COMPRESS_ENABLED = True
STATICFILES_FINDERS = ("compressor.finders.CompressorFinder",)

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

5. Init tailwindcss


```bash
pnpm install -D tailwindcss
npx tailwindcss init
```


6. Update `tailwind.config.js` like so:


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

7. Run the following command to watch for changes and compile the Tailwind CSS code:

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch
```

### HTMLX

1. Download `https://unpkg.com/htmx.org@1.9.10/dist/htmx.js` and save to `static/src`