from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=find_dotenv(),  # BASE_DIR/'.env',
            verbose=True,
            override=True)  # Whether to override the system environment variables with the variables|This will override the cached values and you can access the new .env values every time you run the script


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')

# Application definition

INSTALLED_APPS = [
    # 3rd party apps.........
    "daphne",
    # default apps.........
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # additional apps.........
    # 'django.contrib.humanize',
    # 3rd party apps.........
    "channels",
    'django_extensions',
    "compressor",
    'django_celery_beat',
    'django_celery_results',
    # local apps.........
    "users",
    "status"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <-- new
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # new
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Check if DATABASE_URL is specified and not empty in .env for PostgreSQL
if os.getenv('DATABASE_URL'):
    if DEBUG:
        print('Using [PostgreSQL]...')
        # print(os.getenv("DATABASE_URL"))
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(default=os.environ['DATABASE_URL'])

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"  # the URL to use when referring to static files located in STATICFILES_DIRS
STATICFILES_DIRS = [  # where to find static files
    BASE_DIR / "static",
]
if not DEBUG:
    STATIC_ROOT = BASE_DIR / "staticfiles"
    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# django-compressor
if DEBUG:
    COMPRESS_ROOT = BASE_DIR / "static"
    COMPRESS_ENABLED = True
else:
    COMPRESS_ROOT = STATIC_ROOT
    COMPRESS_ENABLED = False
# Django uses the STATICFILES_FINDERS setting to locate static files in addition to those it finds in STATICFILES_DIRS. By default, it includes `FileSystemFinder` (for files in `STATICFILES_DIRS`) and `AppDirectoriesFinder` (for files in the ‘static’ subdirectory of each app including 'admin' and other dependencies). If you haven’t changed this setting, Django should automatically find static files in your apps. However, if you’ve changed it, that might be causing your problem.
# Although the `AppDirectoriesFinder` is included by default, if we add custom setting like adding the compressor finder, we need to include the 'FileSystemFinder', `AppDirectoriesFinder` explicitly along with the compressor finder.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder"
]

MEDIA_ROOT = BASE_DIR / "uploads"
MEDIA_URL = "/media/"

# Check if DEBUG mode is enabled
if DEBUG:
    # Add Debug Toolbar configuration
    # This will only be enabled in development mode
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    INSTALLED_APPS += ['debug_toolbar', 'django_browser_reload']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',
                   "django_browser_reload.middleware.BrowserReloadMiddleware"]

LOGIN_URL = "users/login"  # new

# Django Channels [START]
ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
# Django Channels [END]

# Django Celery:

# save Celery task results in Django's database
CELERY_RESULT_BACKEND = "django-db"

# This configures Redis as the datastore between Django + Celery
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_REDIS_URL', 'redis://localhost:6379')

# this allows you to schedule items in the Django admin.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

if not DEBUG:
    # log in console
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "INFO",
            },
        },

    }
