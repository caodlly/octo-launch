from environ import Env
import os
from pathlib import Path

# === Change Environment =========================================

BUILD_ENVIRONMENT = os.environ.get("BUILD_ENVIRONMENT", "development").lower()
if BUILD_ENVIRONMENT == "development":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# === BASE_DIR ===================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# === Get .env  ===================================================
env = Env()
Env.read_env(os.path.join(BASE_DIR, ".env"))
# === secret =====================================================
SECRET_KEY = env(
    "SECRET_KEY", default="xi!i5mux!+r2h=13+$%7@w)3u4eur20#v&6at43h-a+%9*kash"
)
# === DEBUG Tools ================================================
DEBUG = False
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
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_celery_beat",
    "sentry_sdk",
]

LOCAL_APPS = [
    "apps.authentications",
    "apps.users",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# === MIDDLEWARE ===========================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
            ],
        },
    },
]
# === ROOT URLCONF ===========================================
ROOT_URLCONF = "config.urls"
# === WSGI APPLICATION ===========================================
WSGI_APPLICATION = "config.wsgi.application"
# === Database ===========================================
DATABASES = {"default": env.db_url("DATABASE_URL")}
# ===AUTH MODEL=====================================================
AUTH_USER_MODEL = "users.User"
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
# === Internationalization ===========================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
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
CELERY_BROKER_URL = env("REDIS_URL")
CELERY_RESULT_BACKEND = env("REDIS_URL")
CELERY_CONFIG = {"broker_connection_retry_on_startup": True}
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

# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
#     'rest_framework.renderers.JSONRenderer']
# ===DRF SPECTACULAR======================================================
SPECTACULAR_SETTINGS = {
    "TITLE": "App Name API",
    "VERSION": "V1.0",
}
# === THROTTLING ======================================================
LOGIN_THROTTLING = 10
LOGIN_THROTTLING_IN = "hour"
