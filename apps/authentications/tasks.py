import uuid
from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from apps.users.models import User
from .models import VerificationCode
from .serializers import VerificationCodeSerializer


@shared_task
def remove_verification_code(id):
    try:
        VerificationCode.objects.get(id=id).delete()
    except VerificationCode.DoesNotExist:
        pass
    return


@shared_task
def send_verification_email(user_email):
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return "Email_DoesNotExist"

    code = str(uuid.uuid4())[:6]

    data = {"user": user.id, "code": code}
    serializer = VerificationCodeSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        id = serializer.data.get("id")
        remove_verification_code.apply_async(
            args=[id], countdown=timedelta(minutes=10).seconds
        )

    else:
        try:
            code_obj = VerificationCode.objects.get(user=user)
            code = code_obj.code
        except VerificationCode.DoesNotExist:
            return "VerificationCode_DoesNotExist"

    return send_mail(
        subject="Verification Code",
        message=f"Your verification code is: {code}",
        from_email=settings.EMAIL_HOST,
        recipient_list=[user.email],
        fail_silently=True,
    )
