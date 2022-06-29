

from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import CustomUser
from django.core.mail import send_mail


@receiver(post_save, sender=CustomUser)
def send_welcome_mail(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Welcome to Goodreads Clone",
            f"Assalamu alaykum, {instance.first_name}! Welcome to Goodreads Clone. Endjoy book and reviews",
            "mohammedyousef.dev@gmail.com",
            [instance.email],
            )
