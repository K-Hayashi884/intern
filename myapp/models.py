from django.db import models

class User(models.Model):
    Username = models.CharField(max_length=128)
    EmailAdress = models.EmailField(max_length=128)
    Password = models.CharField(max_length=128)
    PasswordConfirmation = models.CharField(max_length=128)
    Img = models.ImageField(upload_to='images')


# Create your models here.
