from django import forms
from django.core.validators import MinLengthValidator

class signup (forms.Form):
    name=forms.CharField(label='name')
    e_mail=forms.EmailField(label='e_mail')
    password=forms.CharField(label='password',validators=[MinLengthValidator(8)])
