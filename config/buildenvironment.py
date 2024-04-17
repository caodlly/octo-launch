import os 


def chanageSettingsBasedOnEnvironment():
    BUILD_ENVIRONMENT = os.environ.get("BUILD_ENVIRONMENT", "production").lower()
    if BUILD_ENVIRONMENT == "development":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")