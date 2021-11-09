from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    image=forms.ImageField()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget.attrs.update({
            'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
        self.fields["email"].widget.attrs.update({
            'class':"shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
        self.fields["password1"].widget.attrs.update({
            'class':"shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
        self.fields["password2"].widget.attrs.update({
            'class':"shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })

#     # name=forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control mb-4'}))
#     # mail=forms.EmailField(label='Email address',widget=forms.TextInput(attrs={'class':'form-control mb-4'}))
#     # password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control mb-4'}))
#     # password2=forms.CharField(label="Password confirmation",widget=forms.PasswordInput(attrs={'class':'form-control mb-4'}))
#     # image=forms.ImageField(label="img",widget=forms.FileInput(attrs={'class':'mb-4'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2',"image"]
