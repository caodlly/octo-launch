"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from config.buildenvironment import chanageSettingsBasedOnEnvironment

chanageSettingsBasedOnEnvironment()

# os.environ.setdefault(f"DJANGO_SETTINGS_MODULE", "config.settings.{Build_env}")

application = get_wsgi_application()
