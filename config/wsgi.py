import os

from django.core.wsgi import get_wsgi_application
from octo.base import get_settings_module

os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_settings_module())

application = get_wsgi_application()
