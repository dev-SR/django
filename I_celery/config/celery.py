import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery = Celery('config')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery.config_from_object('django.conf:settings', namespace='CELERY')

# Load `tasks.py` modules from all registered Django apps
celery.autodiscover_tasks()

# We used CELERY_BROKER_URL in settings.py instead of:
# celery.conf.broker_url = ''

# We used CELERY_BEAT_SCHEDULER in settings.py instead of:
# celery.conf.beat_scheduler = ''django_celery_beat.schedulers.DatabaseScheduler'
