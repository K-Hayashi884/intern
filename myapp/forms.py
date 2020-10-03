from django import forms
from django.core.validators import MinLengthValidator

class signup (forms.Form):
    name=forms.CharField(label='name',widget=forms.TextInput(attrs={'class':'form-control'}))
    e_mail=forms.EmailField(label='e_mail',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='password',validators=[MinLengthValidator(8)]\
        ,widget=forms.TextInput(attrs={'class':'form-control'}))
    img=forms.ImageField(verbose_name='画像',null=True,blank=True,upload_to="images")
