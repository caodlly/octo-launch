from octo.handler.manager import Manager
from .command import CreateSuperUser, DBConnect


_manager = Manager()
_manager.set_schema(
    {
        "createsuperuser": CreateSuperUser,
        "check_database": DBConnect,
    }
)


def manager(func):
    """Decorator to configure and customize the behavior of the manage.py file in Django.

    This is used to change basic behavior in manage.py so if you want to create instructions
    specific to your application see here:
    https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/
    """

    def wrapper():
        try:
            return _manager.setup()
        except Exception as e:
            if str(e) in "foo":
                return func()
            print(e)
        return exit(0)

    return wrapper
