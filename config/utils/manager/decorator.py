from .manager import Manager as ManagerTemplate
from django.core.exceptions import ValidationError


class Manager(ManagerTemplate):
    def __init__(self):
        super().__init__()
        schema = {"createsuperuser": "create_superuser"}
        self.set_schema(schema)

    def create_superuser(self):
        """Create a superuser for the Django application."""

        from apps.users.models import User
        from django.conf import settings

        try:
            User.objects.create_superuser(email=settings.ADMIN_EMAIL)
        except ValidationError as e:
            raise ValueError(e.message)


def manager(func):
    """Decorator to configure and customize the behavior of the manage.py file in Django."""

    def wrapper():
        try:
            Manager().setup()
        except ValueError as e:
            if str(e) in "foo":
                return func()
            print(e)

    return wrapper
