import sys


def cancel_create_superuser(func):
    """Decorator to prevent the creation of a superuser under certain conditions."""

    def file_missing_error():
        return print("You can only use this on the manage.py file")

    def cancel():
        return print("You cannot create a super user")

    if 'manage.py' not in sys.argv[0]:
        return file_missing_error

    if len(sys.argv) > 1 and sys.argv[1] == "createsuperuser":
        return cancel
    return func
