from .base import *  # noqa: F403
from .base import INSTALLED_APPS, MIDDLEWARE
from config.utils.storages import *  # noqa: F403
import os

ADMIN_URL = 'admin'
# === DEBUG Tools ================================================
DEBUG = True
nginx_ip = os.environ.get('NGINX_IP', '172.14.3.2')
INTERNAL_IPS = ["127.0.0.1", "0.0.0.0", f"{nginx_ip}",]
INSTALLED_APPS += ['debug_toolbar',]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
