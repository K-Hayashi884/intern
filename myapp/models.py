from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField


class User(AbstractUser):
    image = models.ImageField(default='', blank=True, upload_to='images/')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=CASCADE, null=True, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=CASCADE, null=True, related_name='reciever')
    message = models.CharField(max_length=500)
    message_date = models.DateTimeField(auto_now_add=True)


# Create your models here.
