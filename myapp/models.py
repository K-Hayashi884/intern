from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.base_user import  AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone

class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True, validators=[UnicodeUsernameValidator()])

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    email = models.EmailField(max_length=100)
    img = models.ImageField(upload_to='img/upload/', height_field=None, width_field=None, max_length=100)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    IMAGE_FIELD = 'img'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Message(models.Model):
    send_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_to')
    send_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_from')
    message = models.CharField(max_length=1000)
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'to:' + str(self.send_to) + ', from:' + str(self.send_from) + ', message:' + str(self.message) + ', date:' + str(self.posted_date)

    class Meta:
        ordering = ['posted_date',]
