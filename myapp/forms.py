from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        Username = forms.CharField(max_length=128, required=True)
        EmailAdress = forms.EmailField(max_length=128, required=True)
        Password = forms.CharField(max_length=128, min_length=8, widget=forms.PasswordInput, required=True)
        PasswordConfirmation = forms.CharField(max_length=128, min_length=8, widget=forms.PasswordInput, required=True)
        model = User
        fields = '__all__'
