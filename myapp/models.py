from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='userimg/', default='myapp/static/myapp/img/defaultuser.png')
    regtime = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural = 'CustomUser'

class Message(models.Model):
    # ForeignKeyを2種類作成するために、related_nameを別々で指定しておく
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="receiver")
    sendtime = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=1000)
