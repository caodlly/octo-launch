from django.db import models
from apps.users.models import User
from django.utils.translation import gettext_lazy as _


class VerificationCode(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="code_verified"
    )
    code = models.CharField(_("Code"), max_length=6, blank=True)
    created = models.DateTimeField(_("The time it was created"), auto_now_add=True)

    class Meta:
        ordering = ["-created", "user"]
        indexes = [
            models.Index(fields=["user"]),
        ]
