from django import forms
from .models import User, MyUserManager
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'img', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
        _('This account is inactive.'),
        code='inactive',
        )
