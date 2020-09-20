from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    img = models.ImageField(upload_to='images', null=True, blank=True, default='images/noimage.jpg')

class Talk(models.Model):
    sender = models.CharField(max_length=128)
    recipient = models.CharField(max_length=128)
    content = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True, blank=True)
    time = models.TimeField(auto_now_add=True, blank=True)

# Create your models here.
