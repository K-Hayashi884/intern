from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, \
        validators=[RegexValidator(r'^[a-z]*$')])
    mail = models.EmailField(max_length=200,\
        validators=[EmailValidator()])
    password = models.CharField(max_length=20, \
        validators=[MinLengthValidator(8)])
    image = models.ImageField(verbose_name = 'image', upload_to = 'images/', default=None, null=True,blank=True)
    def __str__(self):
        return '<User:id= ' + str(self.id) + ', ' + self.name + '(' + str(self.mail) + ')>'