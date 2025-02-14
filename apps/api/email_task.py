from celery import shared_task
from django.core.mail import send_mail

from conf.settings import DEFAULT_FROM_EMAIL

@shared_task
def send_email_task(subject, message, recipient_list):
    """
     Task to send email
    """
    print("Sending Email {}".format(recipient_list))
    return send_mail(
        subject=subject,
        message=message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list= recipient_list,
        fail_silently=False
    )