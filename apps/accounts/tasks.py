from celery import shared_task
from django.template.loader import render_to_string
from config.settings.base import APP
from apps.utils.email import send_email


@shared_task
def remove_verification_code(id):
    from .models import VerificationCode

    try:
        VerificationCode.objects.get(id=id).delete()
    except VerificationCode.DoesNotExist:
        return False
    return True


@shared_task
def send_verification_email(email: str):
    from .utils import get_verification_code

    code_obj, user = get_verification_code(email)
    if code_obj and user:
        subject = f"{APP.name} - Verification Code"
        context = {
            "name": user.name,
            "app_name": APP.name,
            "code": code_obj.code,
        }
        html_message = render_to_string(
            "email/send_verification_code.html", context=context
        )
        return send_email(subject, [email], html_message)
    return False


@shared_task
def send_code_reset_password(email: str):
    from .utils import get_verification_code

    code_obj, user = get_verification_code(email)
    if code_obj and user:
        subject = f"{APP.name} - Code Reset Password"
        context = {
            "name": user.name,
            "app_name": APP.name,
            "code": code_obj.code,
        }
        html_message = render_to_string(
            "email/send_code_reset_password.html", context=context
        )
        send_email(subject, [email], html_message)
        return True
    return False
