from django.db import models
from django.conf import settings

# Create your models here.

class UserImage(models.Model):
	username = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	image = models.ImageField(upload_to = '')

	def __str__(self):
		return self.username.__str__()

class Talk(models.Model):
	from_talk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='from_talk')
	to_talk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='to_talk')
	date = models.DateTimeField(auto_now_add=True)
	message = models.CharField(max_length = 500)

	def __str__(self):
		return self.from_talk.username + '(' + self.to_talk.username + ') : ' + self.message
