import sys
import django
from django.core.exceptions import ValidationError


def create_superuser(func):
    """Decorator to prevent the creation of a superuser under certain conditions."""

    def file_missing_error():
        return print("You can only use this on the manage.py file")

    def create() -> None:
        """Create a superuser for the Django application."""
        django.setup()
        from apps.users.models import User
        from django.conf import settings

        try:
            User.objects.create_superuser(email=settings.ADMIN_EMAIL)
        except ValidationError as e:
            return print(e.message)
        return

    if "manage.py" not in sys.argv[0]:
        return file_missing_error

    if len(sys.argv) > 1 and sys.argv[1] == "createsuperuser":
        return create
    return func
