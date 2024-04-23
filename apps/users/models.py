from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from typing import ClassVar
from .managers import UserManager


class User(AbstractUser):
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    username = None  # type: ignore[assignment]
    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), null=True, blank=False, max_length=255)
    email = models.EmailField(_("email address"), null=True, blank=False, unique=True)
    avatar = models.ImageField(default="avatar.svg", upload_to="avatar/")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()
