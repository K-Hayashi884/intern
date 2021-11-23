from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CustomUser(AbstractUser):

    class Meta:
        verbose_name_plural = 'CustomUser'

    icon = models.ImageField(
        verbose_name="画像", upload_to="uploads", 
    )
