from django import forms
from .models import Member

class SignupForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'mail', 'password', 'password_conf', 'img']
