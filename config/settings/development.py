from .base import *  # noqa: F403
from .base import INSTALLED_APPS, MIDDLEWARE
from config.utils.storages import *  # noqa: F403

ADMIN_URL = 'admin'
# === DEBUG Tools ================================================
DEBUG = True
INTERNAL_IPS = ["127.0.0.1", "0.0.0.0", "172.14.4.24",]
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'