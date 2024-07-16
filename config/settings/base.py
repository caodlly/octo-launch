from environ import Env
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from config import app
from datetime import timedelta

# === BASE_DIR ===================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# === Get .env  ===================================================
env = Env()
Env.read_env(os.path.join(BASE_DIR, ".envs/.env"))
# === secret =====================================================
SECRET_KEY = env(
    "SECRET_KEY", default="xi!i5mux!+r2h=13+$%7@w)3u4eur20#v&6at43h-a+%9*kash"
)
# === GENERAL ================================================
DEBUG = env("DEBUG", default=False)
ADMIN_EMAIL = env("ADMIN_EMAIL", default="admin@email.com")
ADMIN_DASHBORD = env("ADMIN_DASHBORD", default=False)
SITE_ID = 1
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en"
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
LANGUAGES = [
    ("en", _("English")),
    ("ar", _("Arabic")),
]
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]
# === URLs Allowed Hosts ==========================================
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
# === CORS Headers ================================================
CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]  # Frontend Domain
CORS_ORIGIN_ALLOW_ALL = False
# === Application definition =====================================
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
]

THIRD_PARTY_APPS = [
    # ========
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    # ========
    "django_filters",
    # ========
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # ========
    "sentry_sdk",
    # ========
]

LOCAL_APPS = [
    "app.user",
    "app.account",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# === MIDDLEWARE ===========================================
MIDDLEWARE = [
    # ========
    "corsheaders.middleware.CorsMiddleware",
    # == Basic =======
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # ========
    "django.middleware.locale.LocaleMiddleware",
    # ========
]
# === TEMPLATES ===========================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]
# === AUTHENTICATION ===========================================
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "user.User"

# Cookies last 2 weeks
SESSION_COOKIE_AGE = int(timedelta(weeks=2).total_seconds())
# === ROOT URLCONF ===========================================
ROOT_URLCONF = "config.urls"
# === WSGI APPLICATION ===========================================
WSGI_APPLICATION = "config.wsgi.application"
# === Database ===========================================
DATABASES = {"default": env.db_url("DATABASE_URL")}
# === AUTH PASSWORD VALIDATORS ===========================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# === Default primary key field type ===========================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# ===CACHES================================================
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# ===CELERY================================================
CELERY_CONFIG = {"broker_connection_retry_on_startup": True}

if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("REDIS_URL")
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# https://github.com/celery/celery/pull/6122
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
# CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True

# ===REST FRAMEWORK================================================
REST_FRAMEWORK = {}

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
    "rest_framework.authentication.SessionAuthentication",
    "rest_framework_simplejwt.authentication.JWTAuthentication",
]
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    "rest_framework.permissions.IsAuthenticatedOrReadOnly"
]
REST_FRAMEWORK["DEFAULT_PAGINATION_CLASS"] = (
    "app.utils.pagination.SmallResultsSetPagination"
)
REST_FRAMEWORK["PAGE_SIZE"] = 30
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
REST_FRAMEWORK["DEFAULT_METADATA_CLASS"] = None

# REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
#     "rest_framework.renderers.JSONRenderer"]

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}

# === DRF SPECTACULAR ======================================================
SPECTACULAR_SETTINGS = {
    "TITLE": f"{app.name} API",
    "DESCRIPTION": f"Documentation of API endpoints of {app.name}",
    "VERSION": app.version,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    # "SCHEMA_PATH_PREFIX": "/api/",
}
# === THROTTLING ======================================================
LOGIN_THROTTLING = 15
LOGIN_THROTTLING_IN = "hour"
RESETPASSWORD_THROTTLING = 15
RESETPASSWORD_THROTTLING_IN = "hour"

ENABLE_SOCIAL_LOGIN = env.bool("ENABLE_SOCIAL_LOGIN", default=False)
# === THROTTLING ======================================================
OCTO_OAUTH = {"google": env("OCTO_OAUTH_GOOGLE", default=None)}
