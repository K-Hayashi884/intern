from django.db import models
from django.forms.fields import ImageField
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='icon/')

    def __str__(self):
        return self.username + ' ' + self.password