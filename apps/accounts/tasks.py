from datetime import timedelta
from celery import shared_task
from apps.users.models import User
from .models import VerificationCode
from .serializers import VerificationCodeSerializer
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from config.settings.base import APP
from apps.utils.generate import generate_code


@shared_task
def remove_verification_code(id):
    try:
        VerificationCode.objects.get(id=id).delete()
    except VerificationCode.DoesNotExist:
        pass
    return


@shared_task
def send_verification_email(user_email: str):
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return "Email_DoesNotExist"

    code = generate_code()

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

    subject = f"{APP.name} - Verification Code"
    context = {
        "name": user.name,
        "app_name": APP.name,
        "code": code,
    }
    html_message = render_to_string(
        "email/send_verification_code.html", context=context
    )
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=subject, body=plain_message, from_email=APP.name, to=[user_email]
    )
    message.attach_alternative(html_message, "text/html")

    try:
        message.send()
        return True
    except Exception as e:
        print("An error occurred while sending email:", e)
        return False
