from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser, Permission, Group
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
    )

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        blank=True,
    )



    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        super().save()

    @property
    def get_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token.key


@receiver(post_save, sender=CustomUser)
def generate_token(sender, instance, created, **kwargs):
    """
    Signal handler to create another object when an instance of YourModel is created.
    """
    if created:
        token = Token.objects.create(user=instance)
        print(token)


class Chat(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    chat_name = models.CharField(max_length=500, blank=True, null=True)
    participants = models.ManyToManyField(CustomUser, related_name='chats', blank=True)
    is_group_chat = models.BooleanField(default=False)

    @property
    def last_message(self):
        return self.messages.all().order_by('id').last()
    @property
    def first_user(self):
        if self.is_group_chat == False:
            return self.participants.first()
        return
    @property
    def second_user(self):
        if self.is_group_chat == False:
            return self.participants.last()
        return


    def __str__(self):
        if self.is_group_chat:
            return f"Group Chat {self.id}"
        else:
            return f"User Chat {self.id}"
    
    def save(self, *args, **kwargs):
        super().save()
        self.chat_name = f'chat{self.id}'
        super().save()

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender} in {self.chat}"
