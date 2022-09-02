from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(email,email_token):
    subject = "Your Account Need to be Verified"
    from_email = settings.EMAIL_HOST_USER
    message = f'Hi Click on the Link to activate your Account http://127.0.0.1:8000/accounts/activate/{email_token}'
    send_mail(subject, message, from_email, [email])