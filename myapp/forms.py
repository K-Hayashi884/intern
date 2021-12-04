from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import Profile
from .models import Message
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(UserCreationForm):
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
        model=Profile
        fields = ['username','email','password1','password2','image']

class LoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget.attrs.update({
            'class':"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
        self.fields["password"].widget.attrs.update({
            'class':"shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })

class MessageForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["content"].widget.attrs.update({
            'class':"shadow border-gray-500 border rounded w-full py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })

    class Meta:
        model=Message
        fields=['content']

class UserChangeForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget.attrs.update({
            'class':"shadow appearance-none border rounded w-full py-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
        self.fields["email"].widget.attrs.update({
            'class':"shadow appearance-none border rounded w-full py-2 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
        self.fields["password1"].widget.attrs.update({
            'class':"shadow appearance-none border rounded w-full py-2 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
        self.fields["password2"].widget.attrs.update({
            'class':"shadow appearance-none border rounded w-full py-2 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline",
            'placeholder':""
        })
    
    class Meta:
        model=Profile
        fields = ['username','email','image','password1']

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = "shadow appearance-none border rounded w-full py-2 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
        self.fields['new_password2'].widget.attrs['class'] = "shadow appearance-none border rounded w-full py-2 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
        self.fields['old_password'].widget.attrs['class'] = "shadow appearance-none border rounded w-full py-2 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"