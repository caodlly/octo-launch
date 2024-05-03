from django.core.wsgi import get_wsgi_application
from config.utils.general import get_settings_module
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_settings_module())

application = get_wsgi_application()
