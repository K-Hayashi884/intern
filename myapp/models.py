from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.
class member (models.Model):
    username=models.CharField(max_length=20)
    mail = models.EmailField(max_length=100)
    password = models.CharField(max_length=50,blank=True,null=True,validators=[MinLengthValidator(8)])
    image=models.ImageField(upload_to="images")

    def __str__(self):
        return 'self.username'