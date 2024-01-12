from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import *


@receiver(post_save, sender=CustomUser)
def generate_token(sender, instance, created, **kwargs):
    """
    Signal handler to create another object when an instance of YourModel is created.
    """
    if created:
        token = Token.objects.create(user=instance)
        print(token)