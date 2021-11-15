from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    image=models.ImageField(upload_to='images/', default='', blank=True, null=True,)


# Create your models here.