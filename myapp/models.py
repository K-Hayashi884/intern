from django.db import models
from django.contrib.auth.models import AbstractUser

class Friend(AbstractUser):
    img = models.ImageField(upload_to='image',default='image/bo2.jpg')
    class Meta:
      verbose_name_plural = 'FriendsList'

class Message(models.Model):
    senduser_name= models.CharField(max_length=100)
    content= models.CharField(max_length=200)
    senduser_id= models.IntegerField()
    reseaveuser_id= models.IntegerField()
    pub_date= models.DateTimeField(auto_now_add=True)
    class Meta:
      ordering=('-pub_date',)
