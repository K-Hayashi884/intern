from django.db import models
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from django.db.models.fields import related
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager
from django.db import models



class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.title

class Photo(models.Model):
    image = models.ImageField(upload_to='photo')
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name="photo")

class Message(models.Model):
    fromusername = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="from1")
    tousername = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="to1")
    content = models.CharField(max_length=300)
    pub_date = models.DateField(default=timezone.now)
    class Meta:
        ordering =  ('pub_date',)

# Create your models here.
  