from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import (
  FileExtensionValidator
)
from django.contrib.auth.forms import AuthenticationForm
from .models import User, UserImage, prof_msg, HeaderImage, Hobby, Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm
from .con import PREFECTURES_CHOICE

class SignUpForm(UserCreationForm):
   image = forms.ImageField( required=False, validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],)
   class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
     super().__init__(*args, **kwargs)
     self.fields['username'].widget.attrs['class'] = 'form-control'
     self.fields['password'].widget.attrs['class'] = 'form-control'

class TalkForm(forms.Form):
  talk = forms.CharField(label='talk')

class PasswordChangeForm(PasswordChangeForm):
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
           field.widget.attrs['class'] = 'form-control'

class NameChangeForm(ModelForm):
  class Meta:
    model = User
    fields = [
      'username',
    ]
  
  def __init__(self, username=None, *args, **kwargs):
    kwargs.setdefault('label_suffix', '')
    super().__init__(*args, **kwargs)
    # ユーザーの更新前情報をフォームに挿入
    if username:
      self.fields['username'].widget.attrs['value'] = username

  def name_update(self, user):
    user.username = self.cleaned_data['username']
    user.save()

class EmailChangeForm(ModelForm):
  class Meta:
    model = User
    fields = [
      'email',
    ]
  
  def __init__(self, email=None,  *args, **kwargs):
    kwargs.setdefault('label_suffix', '')
    super().__init__(*args, **kwargs)
    # ユーザーの更新前情報をフォームに挿入

    if email:
      self.fields['email'].widget.attrs['value'] = email

  def email_update(self, user):
    user.email = self.cleaned_data['email']
    user.save()

class IconChangeForm(ModelForm):
  class Meta:
    model = UserImage
    fields = [
      'image',
    ]

  # def __init__(self, image=None, *args, **kwargs):
  #   kwargs.setdefault('label_suffix', '')
  #   super().__init__(*args, **kwargs)
  #   # ユーザーの更新前情報をフォームに挿入
  #   if image:
  #     self.fields['image'].widget.attrs['value'] = image

  def icon_update(self, user):
    user_img = UserImage.objects.get(user=user)
    user_img.image = self.cleaned_data['image']
    user_img.save()

class HeaderChangeForm(ModelForm):
  class Meta:
    model = HeaderImage
    fields = [
      'image',
    ]

  # def __init__(self, image=None, *args, **kwargs):
  #   kwargs.setdefault('label_suffix', '')
  #   super().__init__(*args, **kwargs)
  #   # ユーザーの更新前情報をフォームに挿入
  #   if image:
  #     self.fields['image'].widget.attrs['value'] = image

  def header_update(self, user):
    user_img = HeaderImage.objects.get(user=user)
    user_img.image = self.cleaned_data['image']
    user_img.save()


class Prof_msgChangeForm(ModelForm):
  class Meta:
    model = prof_msg
    fields = [
      'prof_msg',
    ]

  def __init__(self, prof_msg=None, *args, **kwargs):
    kwargs.setdefault('label_suffix', '')
    super().__init__(*args, **kwargs)
    # ユーザーの更新前情報をフォームに挿入
    if prof_msg:
      self.fields['prof_msg'].widget.attrs['value'] = prof_msg

  def prof_msg_update(self, user):
    msg = prof_msg.objects.get(user=user)
    msg.prof_msg = self.cleaned_data['prof_msg']
    msg.save()

class ProfileChangeForm(ModelForm):
  class Meta:
    model = Profile
    fields = [
      'birthday', 'age', 'location', 'hobby',
    ]

  def __init__(self, birthday=None, age=None, location=None, hobby=None, *args, **kwargs):
    kwargs.setdefault('label_suffix', '')
    super().__init__(*args, **kwargs)
    # ユーザーの更新前情報をフォームに挿入
    if birthday:
      self.fields['birthday'].widget.attrs['value'] = birthday
    if age:
      self.fields['age'].widget.attrs['value'] = age
    if location:
      self.fields['location'].widget.attrs['value'] = location
    if hobby:
      self.fields['hobby'].widget.attrs['value'] = hobby.name

  def profile_update(self, user):
    profile = Profile.objects.get(user=user)
    profile.age = self.cleaned_data['age']
    profile.birthday = self.cleaned_data['birthday']
    profile.location = self.cleaned_data['location']
    profile.hobby.set(self.cleaned_data['hobby'])
    profile.save()


class FindForm(forms.Form):
  find_name = forms.CharField(label='Name', required=False, widget=forms.TextInput)
  find_age = forms.IntegerField(label='Age', required=False, widget=forms.NumberInput)
  find_location = forms.ChoiceField(label='Location', required=False, widget=forms.Select(), choices=(PREFECTURES_CHOICE))
  find_hobby = forms.ChoiceField(label='Hobby', required=False, widget=forms.Select())

class AddHobbyForm(ModelForm):
  class Meta:
    model = Hobby
    fields = [
      'name',
    ]

  # def add_hobby(self):