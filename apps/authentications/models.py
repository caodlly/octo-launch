from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class VerificationCode(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='code_verified')
    code = models.CharField(max_length=6, null=True, blank=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
