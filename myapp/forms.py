from django import forms
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import(AuthenticationForm)
from .models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,AuthenticationForm
from django.core.exceptions import ValidationError


class signup (UserCreationForm):
    class Meta():
        model = User
        fields = ("username", "mail", "image")


class loginform(AuthenticationForm):
    def confirm_login_allowed(self,user):
        if not user.is_active:
            raise ValidationError(("you make a mistake"),code='inactive',)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password'].widget.attrs['class']='form-control'
        
class TalkForm(forms.Form):
    talk=forms.CharField(label='talk')


class Change(PasswordChangeForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.valuse():
            field.widget.attrs['class']='form-control'