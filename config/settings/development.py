from .base import *  # noqa: F403
from .base import INSTALLED_APPS, MIDDLEWARE
from config.utils.storages import *  # noqa: F403


# === GENERAL ================================================
ADMIN_URL = "admin"
ADMIN_DASHBORD = True
# === DEBUG Tools ================================================
INTERNAL_IPS = [
    "127.0.0.1",
    "173.14.0.1",
]
INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
# === Email ================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mailpit"
EMAIL_PORT = 1025
# === SECURITY ================================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
