from django import forms
from django.core.validators import MinLengthValidator

class signup (forms.Form):
    name=forms.CharField(label='name',widget=forms.TextInput(attrs={'class':'form-control'}))
    e_mail=forms.EmailField(label='e_mail',widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='password',validators=[MinLengthValidator(8)]\
        ,widget=forms.TextInput(attrs={'class':'form-control'}))

