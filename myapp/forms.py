from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,PasswordChangeForm,AuthenticationForm
    )
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator
)
from .models import User,UserImage

class SignUpForm(UserCreationForm):
    img = forms.ImageField(
        required=False, validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       #htmlの表示を変更可能にします
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'

class MailSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
           default_label = str(field.label)
           new_label = "new" + default_label
           field.label = new_label

class UserNameSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
           default_label = str(field.label)
           new_label = "new" + default_label
           field.label = new_label

class ImageSettingForm(forms.ModelForm):
    class Meta:
        model = UserImage
        exclude = ("user",)

class PasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
