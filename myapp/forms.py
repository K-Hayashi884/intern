from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from .models import CustomUser, Message
from django.contrib.auth.forms import get_user_model

class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    img = forms.ImageField(label='Img')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'img',)

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':2})
        }

class UsernameChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('username',)

class UsermailChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('email',)

class UsericonChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('img',)

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
