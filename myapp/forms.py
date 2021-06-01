from .models import User
from django import forms

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    image = forms.ImageField(required=True)
    class Meta:
        model = User
        fields = ['name', 'mail', 'password','image']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'mail': forms.EmailInput(attrs={'class':'form-control'}),
        }
#ログイン
class LogInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['name', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
        }
