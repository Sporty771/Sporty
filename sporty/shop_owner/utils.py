# shop_owner/utils.py
from django.core.mail import send_mail

def send_otp_email(email, otp):
    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp}"
    from_email = "no-reply@example.com"
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
