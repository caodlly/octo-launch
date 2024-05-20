from .manager import Manager as ManagerTemplate
from django.core.exceptions import ValidationError
from .database import check_database_connection
from apps.utils.generate import generate_password
from django.contrib.auth.hashers import make_password


class Manager(ManagerTemplate):
    def __init__(self):
        super().__init__()
        self.set_schema(
            {
                "createsuperuser": "create_superuser",
                "check_database": "check_database",
            }
        )

    def create_superuser(self):
        """Create a superuser for the Django application."""
        from apps.users.models import User
        from django.conf import settings

        email = settings.ADMIN_EMAIL
        password = generate_password()

        try:
            user = User.objects.create_superuser(
                email=email, password=make_password(password)
            )
            if user:
                print(f"Email: {email}")
                print(f"Password: {password}")
        except ValidationError as e:
            raise ValueError(e.message)

    @staticmethod
    def check_database():
        """Verify database connection"""
        return check_database_connection()


def manager(func):
    """Decorator to configure and customize the behavior of the manage.py file in Django.

    This is used to change basic behavior in manage.py so if you want to create instructions
    specific to your application see here:
    https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/
    """

    def wrapper():
        try:
            Manager().setup()
        except ValueError as e:
            if str(e) in "foo":
                return func()
            print(e)

    return wrapper
