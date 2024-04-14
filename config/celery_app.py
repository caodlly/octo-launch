import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings



BUILD_ENVIRONMENT = os.environ.get('BUILD_ENVIRONMENT', 'development').lower()
if  BUILD_ENVIRONMENT=="development":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
else : 
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    
app = Celery('app_config')
app.conf.update(**settings.CELERY_CONFIG)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.beat_schedule = {}
