from django.contrib.auth.models import User
from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class UserCreateForm(UserCreationForm):
    image = forms.ImageField(
        required=False
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #htmlの表示を変更可能にします
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta:
       model = User
       fields = ("username", "email", "password1", "password2", "image")

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       #htmlの表示を変更可能にします
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'

class UserChangeForm(forms.ModelForm):
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        self.fields['username'].widget.attrs['class'] = 'form-control'
 
    class Meta:
        model = User
        fields = (
            "username",
        )

class EmailChangeForm(forms.ModelForm):
 
    # 入力を必須にするために、required=Trueで上書き
    email = forms.EmailField(required=True)
 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        self.fields['email'].widget.attrs['class'] = 'form-control'
 
    class Meta:
        model = User
        fields = (
            "email",
        )
 
    def clean_email(self):
        email = self.cleaned_data["email"]
 
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("正しいメールアドレスを指定してください。")
 
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            if self.user.email == email:
                return email
 
            raise ValidationError("このメールアドレスは既に使用されています。別のメールアドレスを指定してください")
 
class UserPasswordChangeForm(PasswordChangeForm):
    pass