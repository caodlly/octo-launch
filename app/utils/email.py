from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from config import app


def send_email(subject: str, to: list, html_message: str):
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject=subject, body=plain_message, from_email=app.name, to=to
    )
    message.attach_alternative(html_message, "text/html")

    try:
        message.send()
        return True
    except Exception as e:
        return f"An error occurred while sending email: {e}"
