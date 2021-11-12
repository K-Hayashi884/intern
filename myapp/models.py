from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone

# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='image/', verbose_name="画像")

    def __str__(self):
        return self.username + ' ' + self.password

class Message(models.Model):
    sender = models.CharField(max_length=150)
    receiver = models.CharField(max_length=150)
    contents = models.CharField(max_length=500)
    date_joined = models.DateTimeField(default=django.utils.timezone.now)