from django.db import models
from django.contrib.auth.models import AbstractUser

class Friend(AbstractUser):
  img = models.ImageField(upload_to='img',default='img/bo2.jpg')
  class Meta:
    verbose_name_plural = 'FriendsList'
