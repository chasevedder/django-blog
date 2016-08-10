from django import forms
from .models import BlogPost, Comment
from customauth.models import MyUser


class PostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']


class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']


class UpvoteForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        # exclude = ['author', 'updated', 'created', ]
        fields = []
