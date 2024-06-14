from .manager import Manager as ManagerTemplate


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
        from .user import create_superuser

        return create_superuser(self._args)

    @staticmethod
    def check_database():
        """Verify database connection"""
        from .database import check_database_connection

        return check_database_connection()


def manager(func):
    """Decorator to configure and customize the behavior of the manage.py file in Django.

    This is used to change basic behavior in manage.py so if you want to create instructions
    specific to your application see here:
    https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/
    """

    def wrapper():
        try:
            return Manager().setup()
        except ValueError as e:
            if str(e) in "foo":
                return func()
            print(e)
        return exit(0)

    return wrapper
