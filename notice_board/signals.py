from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.contrib.auth.models import User
from .models import Author


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=User)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(authorUser=instance)


