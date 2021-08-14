from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator
from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.
class User(AbstractUser):
    #username = models.CharField(max_length=100, \
        #validators=[RegexValidator(r'^[a-z]*$')])
    #mail = models.EmailField(max_length=200,\
        #validators=[EmailValidator()])
    # password = models.CharField(max_length=20, \
    #     validators=[MinLengthValidator(8)])
    image = models.ImageField(verbose_name = 'image', upload_to = 'images/', default=None, null=True, blank=True)
    #def __str__(self):
    #    return '<User:id= ' + str(self.id) + ', ' + self.username + '>'
    #↑↑これいるのか問題→トークルームのnameがこれで出力されるから外す。



class Talk(models.Model):
    talk_from = models.ForeignKey(User, on_delete=models.CASCADE)
    talk = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    talk_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', default=None, null=True) #★
#↑↑これmany to many説ある

    def __str__(self):
        #return '<Message:id= ' + '(' + str(self.pub_date) + ')>'
        return "{}>>{}".format(self.talk_from, self.talk_to)
    class Meta:
        ordering = ('pub_date',)