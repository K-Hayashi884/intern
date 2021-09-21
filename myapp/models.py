from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=8,unique=True)
    password=models.CharField(max_length=100,validators=[MinLengthValidator(8)])
    email=models.EmailField(blank=False,null=False)

class Image(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='img')
    img = models.ImageField(upload_to="images")

class Message(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_from',null=True)
    user_to= models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_to',null=True)
    message=models.CharField(max_length=1000,null=True)
    date=models.DateTimeField(default=timezone.now)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='mes', null=True)
    latest_message = models.BooleanField(null=True)