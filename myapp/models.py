from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    img = models.ImageField(upload_to='img', default='asset/default-image.png')

    class Meta:
        verbose_name_plural='CustomUser'
# Create your models here.
