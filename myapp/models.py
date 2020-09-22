from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    img = models.ImageField(upload_to='images', null=True,
                            blank=True, default='images/noimage.jpg')


class Talk(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='talk_sender')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='talk_recipient')
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True, blank=True)
# Create your models here.
