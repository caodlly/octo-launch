from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.user"

    def ready(self):
        import app.user.signals  # noqa
