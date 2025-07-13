from core.models import OTP
from utils.send_email_ import send_email

def send_otp_email(user):
    """
    Sends a One-Time Password (OTP) to the user's email.

    This function generates a new OTP for the given user (or retrieves an existing one),
    then sends it via email with a validity of 10 minutes.

    :param user: User instance to whom the OTP should be sent
    :type user: User
    :return: None
    :rtype: None
    """
    otp, _ = OTP.objects.get_or_create(user=user)
    otp.generate_otp()

    send_email(
        'Your OTP Code',
        f'Your OTP code is: {otp.otp_code}\nIt will expire in 10 minutes.',
        [user.email],
        fail_silently=False,
    )