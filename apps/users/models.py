from django.db.models import signals
from django.dispatch import receiver
from apps.utils.image import resize_image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from typing import ClassVar
from .managers import UserManager


class User(AbstractUser):
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=False, max_length=90)
    email = models.EmailField(
        _("email address"), blank=False, unique=True, db_index=True
    )
    avatar = models.ImageField(default="avatar.svg", upload_to="avatar/")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()


@receiver(signals.pre_save, sender=User)
def resize_image_before_save(sender, instance, **kwargs):
    try:
        if instance.pk:
            old_instance = sender.objects.get(pk=instance.pk)
            if instance.avatar != old_instance.avatar:
                instance.avatar = resize_image(instance.avatar, 450, 450)
    except Exception as e:
        raise Exception(e.args)
