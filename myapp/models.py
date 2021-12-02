from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import related

class CustomUser(AbstractUser):
    latest = ''
    icon = models.ImageField(upload_to='uploads',default='noimage/noimage.png',blank=True,null=True)

class Talk(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="receiver")
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

# Create your models here.
