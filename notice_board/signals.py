from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.contrib.auth.models import User
from .models import Author, Reply
from django.core.mail import send_mail


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=User)
def notify_managers_appointment(instance, created, **kwargs):
    if created:
        Author.objects.create(authorUser=instance)

@receiver(post_save, sender=Reply)
def notify_managers_appointment(instance, created, **kwargs):
    if created:
        email_for_sent = instance.replyAd.adAuthor.authorUser.email
        send_mail(
            subject=f'Отклик',
            message=f'На Ваше объявлеине с заголовком {instance.replyAd.adTitle} откликнулись',
            from_email='aigulapai@yandex.ru',
            recipient_list=[email_for_sent]
        )


