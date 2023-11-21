import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_settings.settings')

app = Celery('django_settings')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()