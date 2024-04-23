from config.settings.base import env, INSTALLED_APPS, BASE_DIR
import os

INSTALLED_APPS += ["collectfast", "storages"]

TYPE_STORAGE = env("TYPE_STORAGE", default="local")

if TYPE_STORAGE == "s3":
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "location": "media",
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "location": "static",
                "default_acl": "public-read",
            },
        },
    }

    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_QUERYSTRING_AUTH = False
    # DO NOT change these unless you know what you're doing.
    _AWS_EXPIRY = 60 * 60 * 24 * 7
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate",
    }
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_S3_MAX_MEMORY_SIZE = env.int(
        "AWS_S3_MAX_MEMORY_SIZE",
        default=100_000_000,  # 100MB
    )
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default=None)
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#cloudfront
    AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", default=None)

    AWS_S3_HOST = (
        AWS_S3_CUSTOM_DOMAIN
        or f"{AWS_STORAGE_BUCKET_NAME} \
        .s3.amazonaws.com"
    )

    MEDIA_URL = f"{AWS_S3_HOST}/media/"
    STATIC_URL = f"{AWS_S3_HOST}/static/"
    COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"


elif TYPE_STORAGE == "gcp":
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "location": "media",
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "location": "static",
                "default_acl": "publicRead",
            },
        },
    }
    GS_BUCKET_NAME = env("GCP_STORAGE_BUCKET_NAME")
    GS_DEFAULT_ACL = "publicRead"
    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
    COLLECTFAST_STRATEGY = "collectfast.strategies.gcloud.GoogleCloudStrategy"
    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"

elif TYPE_STORAGE == "local":
    STATIC_URL = "static/"
    MEDIA_URL = "/media/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_ROOT = BASE_DIR / "static/media"
    COLLECTFAST_STRATEGY = "collectfast.strategies.filesystem.FileSystemStrategy"

else:
    raise TypeError("Please specify the value of TYPE_STORAGE in the .env file")
