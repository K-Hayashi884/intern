from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "icon")


class LoginForm(AuthenticationForm):        
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       #htmlの表示を変更可能にします
       self.fields["username"].widget.attrs["class"] = "form-control"
       self.fields["password"].widget.attrs["class"] = "form-control"
