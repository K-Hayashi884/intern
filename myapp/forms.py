from .models import User, Talk
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
User = get_user_model()
#from django.contrib.auth.forms import AuthentificationForm 

class SignUpForm(UserCreationForm):
    class Meta:
        image = forms.ImageField(required=True)
        model = User
        fields = ('username','email', 'password1', 'password2', 'image')
        #widgets = {
            #'username': forms.TextInput(attrs={'class':'form-control'}),
            #'mail': forms.EmailInput(attrs={'class':'form-control'}),
            #'password2': forms.PasswordInput()
        #}
#    def save(self, request):
#       # Ensure you call the parent class's save.
        # .save() returns a User object.
#       user = super(SignUpForm, self).save(request)
#       user.image = self.cleaned_data['image']
#       user.save()
#       return user

#class Me   ssageForm(forms.ModelForm):
    #data = User
    #class Meta:
        #model = Message
        #fields = ['content', 'user', 'to']
        #widgets = {
            #'content' : forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            #'to' : forms.Select(attrs={'class':'form-control form-control-sm'}), #★
            #'user' : forms.Select(attrs={'class':'form-control form-control-sm'}),
            #ここのuserをログイン中のuserを自動指定するようにしたい。
        #}
    
class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields= ('talk',)
    talk = forms.CharField(label='talk')
    #talk_from = forms.CharField()
    #pub_date = forms.DateTimeField()
    #talk toに何らかUserのリストから入れることを表現したい
    #talk_to = forms.ChoiceField(label="送信先", widget=forms.Select,  required=True) 

class UserNameSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
           default_label = str(field.label)
           new_label = "new" + default_label
           field.label = new_label

class UserEmailSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
           default_label = str(field.label)
           new_label = "new" + default_label
           field.label = new_label

#class UserPasswordSettingForm(PasswordChangeForm):
#    """パスワード変更フォーム"""
#
#   def __init__(self, *args, **kwargs):
#       super().__init__(*args, **kwargs)
#        for field in self.fields.values():
#            field.widget.attrs['class'] = 'form-control'

class UserImageSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image', )

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
           default_label = str(field.label)
           new_label = "new" + default_label
           field.label = new_label