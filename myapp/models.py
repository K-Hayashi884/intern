from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    image=models.ImageField(upload_to='images/', default='', blank=True, null=True,)

class Message(models.Model):
    sender=models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="sender"
    )
    receiver=models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="receiver"
    )
    content=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

# Create your models here.