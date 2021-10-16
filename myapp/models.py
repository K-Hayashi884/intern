from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.files import ImageField

class User(AbstractUser):
    image = models.ImageField(default='', blank=True, upload_to='images/')


# Create your models here.
