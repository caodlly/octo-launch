from django.core.exceptions import ValidationError
from app.utils.generate import generate_password
from django.contrib.auth.hashers import make_password
from app.user.models import User
from django.conf import settings
from environ import Env
import os
import stat


def _create_superuser(email, password):
    """Create a superuser for the Django application."""
    try:
        return User.objects.create_superuser(
            email=email, password=make_password(password)
        )
    except ValidationError as e:
        raise ValueError(e.message)


def create_superuser():
    """Processing and creating a super user."""

    admin_path_env = os.path.join(settings.BASE_DIR, ".envs/.admin")

    if settings.DEBUG and os.path.exists(admin_path_env):
        env = Env()
        Env.read_env(admin_path_env)

        email = env("email", default=settings.ADMIN_EMAIL)
        password = env("password", default=generate_password())
    else:
        email = settings.ADMIN_EMAIL
        password = generate_password()

    _create_superuser(email, password)

    # Write the email and password to the .admin file
    with open(admin_path_env, "w") as admin_file:
        admin_file.write(f"email='{email}'\n")
        admin_file.write(f"password='{password}'\n")

    # Set file permissions to read/write for the owner only
    if not settings.DEBUG:
        os.chmod(admin_path_env, stat.S_IRUSR | stat.S_IWUSR)

    # Print the email and password for the admin
    print(f"{email}")
    print(f"{password}")
