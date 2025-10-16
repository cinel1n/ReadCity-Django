from django.db import transaction
from django.db.models.signals import post_save
from django.shortcuts import render

from ReadCity import settings
from main.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse


from django.db.models.signals import post_save
from main.models import User
from main.tasks import send_verification_email
from django.dispatch import receiver

@receiver(post_save, sender=User)
def user_update(sender, instance,created, *args, **kwargs):
    if created and not instance.is_verified:
        send_verification_email.delay(instance.pk)


# def send_verification_email(user):
#     """
#     Функция для отправки email с ссылкой верификации
#     """
#     verification_url = 'http://127.0.0.1:8000%s' % reverse(
#         'verify',
#         kwargs={'uuid': str(user.verification_uuid)}
#     )
#
#     send_mail(
#         subject='Verify your account',
#         message=f'Follow this link to verify your account: {verification_url}',
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[user.email],
#         fail_silently=False,
#     )
#     send_mail(
#         'Verify your account',
#         'Follow this link to verify your account: '
#         'http://127.0.0.1:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
#         'readcity.app@gmail.com',
#         [user.email],
#         fail_silently=False,
#     )