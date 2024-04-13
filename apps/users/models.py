from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.exceptions import ObjectDoesNotExist

message_username_validator = 'The Username must contain only lowercase letters and English numbers and you can use: ' \
                             '"-". It must be at least 3 characters long.'

username_regex = r'^[a-z0-9-]{3,}$'


class User(AbstractUser):
    username_validator = RegexValidator(
        regex=username_regex, message=message_username_validator)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True, null=True,
                              blank=False, db_index=True)
    first_name = models.CharField(max_length=15, null=True, blank=False)
    last_name = models.CharField(max_length=15, null=True, blank=False)
    avatar = models.ImageField(default='avatar.svg', upload_to="avatar/")
    customer_id = models.CharField(max_length=255, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username


@receiver(pre_save, sender=User)
def user_post_save(sender, instance, **kwargs):
    try:
        user = User.objects.get(pk=instance.pk)
        if user.email != instance.email:
            instance.email_verified = False
            from authentications.tasks import send_verification_email
            send_verification_email.apply_async(
                args=[instance.email], countdown=5)
    except ObjectDoesNotExist:
        pass
