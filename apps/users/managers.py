from apps.utils import Generate
from typing import TYPE_CHECKING
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.apps import apps
from .tasks import send_password_email
from django.conf import settings

if TYPE_CHECKING:
    from .models import User  # noqa: F401


class UserManager(DjangoUserManager["User"]):
    """Custom manager for the User model."""

    def _create_user(self, email: str, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")

        password = Generate.password()

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )

        email = self.normalize_email(email)
        username = Generate.remove_email(email)
        username = GlobalUserModel.normalize_username(username)
        name = str(email.split("@")[0])
        user = self.model(email=email, username=username, name=name, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        if user.is_superuser and settings.DEBUG:
            print("email: " + email)
            print("password: " + password)
        send_password_email.delay(name, email, password)
        return user

    # type: ignore[override]
    def create_user(self, email: str, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, **extra_fields)

    # type: ignore[override]
    def create_superuser(self, email: str, **extra_fields):
        if self.model.objects.filter(is_superuser=True).exists():
            raise ValidationError("There can be only one superuser.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, **extra_fields)
