from .base import *  # noqa: F403
from .base import INSTALLED_APPS, MIDDLEWARE
from config.utils.storages import *  # noqa: F403


# === Admin ================================================
ADMIN_URL = "admin"
# === DEBUG Tools ================================================
INTERNAL_IPS = [
    "127.0.0.1",
    "0.0.0.0",
    "172.14.3.2",
]
INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
# === Email ================================================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# === SECURITY ================================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
