from django import forms
from .models import BlogPost
from customauth.models import MyUser

class PostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'content']


class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']