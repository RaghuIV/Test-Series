from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

def send_email(subject, message, recipient_list, from_email=None, fail_silently=False, html_message=None):
    """
    Utility function to send an email.

    :param subject: Subject of the email
    :param message: Body of the email
    :param recipient_list: List of recipient email addresses
    :param from_email: Sender's email address (defaults to settings.EMAIL_HOST_USER)
    :param fail_silently: Whether to suppress errors (default is False)
    :param html_message: HTML message (optional)
    :return: None
    """
    if from_email is None:
        from_email = settings.EMAIL_HOST_USER

    try:
        email = EmailMessage(subject, message, from_email, recipient_list)
        if html_message:
            email.content_subtype = 'html'  # Set the content type to HTML
            email.body = html_message
        email.send(fail_silently=fail_silently)
    except Exception as e:
        if not fail_silently:
            raise e

