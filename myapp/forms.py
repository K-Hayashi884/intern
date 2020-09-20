from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# class UserForm(forms.Form):
#     Username = forms.CharField(max_length=128, required=True)
#     EmailAdress = forms.EmailField(max_length=128, required=True)
#     Password = forms.CharField(max_length=128, min_length=8, widget=forms.PasswordInput, required=True)
#     PasswordConfirmation = forms.CharField(max_length=128, min_length=8, widget=forms.PasswordInput, required=True)
#     Img = forms.ImageField(required=False)

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'img', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    pass

class TalkroomForm(forms.Form):
    message = forms.CharField(max_length=1000, label="")

class ChangeNameForm(forms.Form):
    oldpassword = forms.CharField(max_length=128, label="Old Password", widget=forms.TextInput(attrs={'class': 'form-control'}))
    newpassword = forms.CharField(max_length=128, label="New Password", widget=forms.TextInput(attrs={'class': 'form-control'}))
    passwordconfirmation = forms.CharField(max_length=128, label="New Password Confirmation", widget=forms.TextInput(attrs={'class': 'form-control'}))

class ChangeMailForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class ChangeImgForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['img']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class ChangeUsernameForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"