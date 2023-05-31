from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from private import base_link


def send_verification_email(recipient_email, token, user):
    verification_link = f'{base_link}/accounts/verify/{user.id}/{token}'
    subject = 'Email Verification'
    message = render_to_string('accounts/email_verification/verification_email.html', {
        "user": user,
        "verification_link": verification_link,
    })
    plain_message = strip_tags(message)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email="sovuh2703@gmail.com",
        recipient_list=[recipient_email],
        html_message=message,
    )
