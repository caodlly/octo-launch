import os

from celery import Celery
from django.conf import settings

# from celery.schedules import crontab
from octo.base import get_settings_module

os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_settings_module())

app = Celery("app_config")
app.conf.update(**settings.CELERY_CONFIG)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.beat_schedule = {}
