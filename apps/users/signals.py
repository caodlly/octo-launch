from django.db.models import signals
from django.dispatch import receiver
from apps.utils.image import resize_image
from .models import User
from apps.utils.generate import generate_code
from apps.accounts.tasks import send_verification_email


@receiver(signals.pre_save, sender=User)
def pre_save_user(sender: User, instance: User, **kwargs):
    print(instance)
    print(instance.pk)
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
            send_verification_email.delay(instance.email)

    except Exception as e:
        raise Exception(f"Error in post_save signal: {e}")