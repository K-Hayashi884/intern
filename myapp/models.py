from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.files import ImageField

class CustomUser(AbstractUser):
    icon = models.ImageField(upload_to='uploads',default='noimage/noimage.png')



# Create your models here.
