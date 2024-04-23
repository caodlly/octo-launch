import os
import django
from django.core.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

django.setup()


def create_superuser() -> None:
    """Create a superuser for the Django application."""
    from apps.users.models import User
    from django.conf import settings

    try:
        User.objects.create_superuser(email=settings.ADMIN_EMAIL)
    except ValidationError as e:
        return print(e.message)
    return


if __name__ == "__main__":
    create_superuser()
