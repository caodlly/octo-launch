from environ import Env
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# === BASE_DIR ===================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# === Get .env  ===================================================
env = Env()
Env.read_env(os.path.join(BASE_DIR, ".env"))
# === secret =====================================================
SECRET_KEY = env(
    "SECRET_KEY", default="xi!i5mux!+r2h=13+$%7@w)3u4eur20#v&6at43h-a+%9*kash"
)
# === GENERAL ================================================
DEBUG = False
ADMIN_EMAIL = env("ADMIN_EMAIL", default="admin@email.com")
SITE_ID = 1
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
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
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # ========
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "dj_rest_auth",
    # ========
    "django_filters",
    "django_celery_beat",
    # ========
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # ========
    "sentry_sdk",
    # ========
    "django_extensions",
]


LOCAL_APPS = [
    "apps.users",
    "apps.authentications",
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
    "allauth.account.middleware.AccountMiddleware",
]
# === TEMPLATES ===========================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# === allauth ===========================================
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_USERNAME_REQUIRED = False
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env("GOOGLE_CLIENT_ID"),
            "secret": env("GOOGLE_SECRET"),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
        "FETCH_USERINFO": True,
        "OAUTH_PKCE_ENABLED": True,
    }
}

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
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True

# ===REST FRAMEWORK================================================
REST_FRAMEWORK = {}

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
    "rest_framework.authentication.SessionAuthentication",
]
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    "rest_framework.permissions.IsAuthenticatedOrReadOnly"
]
REST_FRAMEWORK["DEFAULT_PAGINATION_CLASS"] = (
    "apps.utils.pagination.SmallResultsSetPagination"
)
REST_FRAMEWORK["PAGE_SIZE"] = 20
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
REST_FRAMEWORK["DEFAULT_METADATA_CLASS"] = None

# REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
#     "rest_framework.renderers.JSONRenderer"]

CORS_URLS_REGEX = r"^/api/.*$"

# === DRF SPECTACULAR ======================================================
SPECTACULAR_SETTINGS = {
    "TITLE": "APP NAME API",
    "DESCRIPTION": "Documentation of API endpoints of [APP NAME]",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    # "SCHEMA_PATH_PREFIX": "/api/",
}
# === THROTTLING ======================================================
LOGIN_THROTTLING = 10
LOGIN_THROTTLING_IN = "hour"
