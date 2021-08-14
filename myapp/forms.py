from .models import User, Talk
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
#from django.contrib.auth.forms import AuthentificationForm 

class SignUpForm(UserCreationForm):
    class Meta:
        image = forms.ImageField(required=True)
        model = User
        fields = ('username', 'password1', 'password2', 'image')
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
    
class TalkForm(forms.Form):
    talk = forms.CharField(label='talk')
