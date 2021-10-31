from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'img')

class LoginForm(AuthenticationForm):
    pass