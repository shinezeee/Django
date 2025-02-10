from django.conf import settings
from django.core.mail import send_mail


# def send_email(subject,message,from_email,to_email):
#   to_email = to_email if isinstance(to_email, list) else [to_email, ]
#   send_mail(subject, message, from_email, to_email)

def send_email(subject,message,to_email):
    # 이메일 전송
    send_mail(
      subject=subject,
      message=message,
      from_email=settings.DEFAULT_FROM_EMAIL,
      recipient_list=[to_email],
      fail_silently=False,
    )

