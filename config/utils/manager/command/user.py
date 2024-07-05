from octo.handler.command import Command


class CreateSuperUser(Command):
    """Class for creating a superuser and managing its details."""

    def __init__(self):
        super().__init__()
        self.print_details = True
        self.no_file = False
        self.remove_admin = False
        self.set_hooks(
            {
                "--no-print": "set_print_details",
                "--no-file": "set_no_file",
                "--rm-admin": "set_remove_admin",
            }
        )

    def handle(self):
        """Processing and creating a super user."""
        # === import =====================================
        from django.core.exceptions import ValidationError
        from octo.utils.generate import generate_password
        from django.contrib.auth.hashers import make_password
        from app.user.models import User
        from django.conf import settings
        from environ import Env
        import os
        import stat

        # === Get User =====================================
        admin_path_env = os.path.join(settings.BASE_DIR, ".envs/.admin")

        if not os.path.exists(admin_path_env):
            with open(admin_path_env, "w"):
                ...

        env = Env()
        Env.read_env(admin_path_env)
        email = env("email", default=settings.ADMIN_EMAIL)

        if self.no_file and self.remove_admin:
            password = generate_password()
        else:
            password = env("password", default=generate_password())

        try:
            User.objects.create_superuser(email=email, password=make_password(password))
        except ValidationError as e:
            raise ValueError(e.message)

        # === Logic =====================================

        if not self.no_file and not self.remove_admin:
            # Write the email and password to the .admin file
            with open(admin_path_env, "w") as admin_file:
                admin_file.write(f"email='{email}'\n")
                admin_file.write(f"password='{password}'\n")

        if settings.DEBUG:
            # Set file permissions to read/write for the owner only
            os.chmod(admin_path_env, stat.S_IRUSR | stat.S_IWUSR)

        if self.print_details or self.remove_admin:
            # Print the email and password for the admin
            print(f"{email}")
            print(f"{password}")

        if self.remove_admin:
            # remove .admin file
            os.remove(admin_path_env)

    def set_print_details(self):
        """Prevent printing of account details"""
        self.print_details = False

    def set_no_file(self):
        """It does not create an .admin file, and if it exists, it deletes it"""
        self.no_file = True
        self.remove_admin = True

    def set_remove_admin(self):
        """It deletes the .admin file after creating the account"""
        self.remove_admin = True
