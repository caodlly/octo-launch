from config.settings.base import env, INSTALLED_APPS, BASE_DIR
import os

INSTALLED_APPS += ["collectfast", "storages"]

TYPE_STORAGE = env("TYPE_STORAGE", default="local")

if TYPE_STORAGE == "s3":
    """
    If you want to protect media files and allow static files to be public,
    you can use these settings and add this configuration to
    Bucket policy:
    
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadForStaticFiles",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::your-bucket-name/static/*"
            }
        ]
    }
    
    # TODO Change -> [your-bucket-name]
    """

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
                "querystring_auth": False,  # This setting does not send authentication keys when requesting static files
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
    # DO NOT change these unless you know what you're doing.
    # AWS_QUERYSTRING_AUTH = True
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

elif TYPE_STORAGE == "local":
    STATIC_URL = "static/"
    MEDIA_URL = "media/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    COLLECTFAST_STRATEGY = "collectfast.strategies.filesystem.FileSystemStrategy"

else:
    raise TypeError("Please specify the value of TYPE_STORAGE in the .env file")
