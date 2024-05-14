from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from config.utils.app import App


@shared_task
def send_password_email(name, email, password):
    subject = f"{App().name} - Your Account Details"
    context = {
        "name": name,
        "email": email,
        "password": password,
        "app_name": App().name,
    }
    html_message = render_to_string("email/send_password.html", context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=subject, body=plain_message, from_email=App().name, to=[email]
    )
    message.attach_alternative(html_message, "text/html")

    try:
        message.send()
        return True
    except Exception as e:
        print("An error occurred while sending email:", e)
        return False
