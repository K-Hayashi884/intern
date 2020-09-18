from django import forms
from .models import User, MyUserManager, Message
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'img', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
        _('This account is inactive.'),
        code='inactive',
        )

class FindForm(forms.Form):
    find = forms.CharField(label='search', required=False)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': '' }

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        labels = {'email': '新しいメールアドレス'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        def clean_email(self):
            email = self.cleaned_data['email']
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError('正しいメールアドレスを指定してください。')

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {'username': '新しいユーザ名'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        def clean_username(self):
            username = self.cleaned_data['username']
            try:
                validate_username(username)
            except ValidationError:
                raise ValidationError('正しいユーザ名を指定してください。')

class IconChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['img']
        labels = {'img': '新しいアイコン'}
