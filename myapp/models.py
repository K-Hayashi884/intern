from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='image/', verbose_name="画像")

    def __str__(self):
        return self.username + ' ' + self.password