from datetime import timedelta


def get_verification_code(email: str):
    from apps.users.models import User
    from .models import VerificationCode
    from .tasks import remove_verification_code

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return False, False

    code_obj, created = VerificationCode.objects.get_or_create(user=user)
    if created:
        remove_verification_code.apply_async(
            args=[code_obj.id], countdown=timedelta(minutes=10).seconds
        )

    return code_obj, user
