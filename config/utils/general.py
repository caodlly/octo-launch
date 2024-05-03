from config.settings.base import DEBUG


def get_settings_module():
    if DEBUG:
        return "config.settings.development"
    return "config.settings.production"
