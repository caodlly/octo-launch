from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.account"
    label = "app_account"  # in order to avoid conflict with the allauth app
    verbose_name = "builtInAccount"
