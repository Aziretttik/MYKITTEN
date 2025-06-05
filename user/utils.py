import random
import string
from django.core.mail import send_mail
from django.conf import settings



def generate_verification_code():
    """Генерирует 6-значный код подтверждения"""
    return ''.join(random.choices(string.digits, k=6))


def send_verification_email(email, code):
    subject = 'Код подтверждения для входа'
    message = f'Ваш код подтверждения: {code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
