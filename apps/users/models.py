from django.db.models import signals
from django.dispatch import receiver
from apps.utils.image import resize_image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from typing import ClassVar
from .managers import UserManager
from apps.utils.generate import generate_code


class User(AbstractUser):
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=False, max_length=90)
    email = models.EmailField(
        _("Email Address"),
        blank=False,
        unique=True,
    )
    email_verified = models.BooleanField(_("Email Verified"), default=False)
    avatar = models.ImageField(_("Avatar"), default="avatar.svg", upload_to="avatar/")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    class Meta:
        ordering = ["-email"]
        indexes = [
            models.Index(fields=["email"]),
        ]


@receiver(signals.pre_save, sender=User)
def pre_save_user(sender: User, instance: User, **kwargs):
    try:
        if instance.pk:
            old_instance = sender.objects.get(pk=instance.pk)

            if instance.avatar != old_instance.avatar:
                instance.avatar = resize_image(instance.avatar, 450, 450)

            if instance.email != old_instance.email:
                instance.email_verified = False
        if not instance.username:
            instance.username = instance.email.split("@")[0] + "_" + generate_code()
    except Exception as e:
        raise Exception(f"Error in pre_save signal: {e}")


@receiver(signals.post_save, sender=User)
def post_save_user(sender: User, instance: User, created, **kwargs):
    try:
        if not instance.email_verified:
            from apps.accounts.tasks import send_verification_email

            send_verification_email.delay(instance.email)

    except Exception as e:
        raise Exception(f"Error in post_save signal: {e}")
