from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def send_otp_email(name, email, otp):
    context = {
        'username': name,
        'otp': otp,
    }
    
    email_subject = 'Your OTP for Password Reset'
    email_body = render_to_string('userpanel/otp_email.html', context)
    
    myemail = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email],
    )
    myemail.content_subtype = "html"  # Important: set the content type to HTML
    return myemail.send(fail_silently=False)
