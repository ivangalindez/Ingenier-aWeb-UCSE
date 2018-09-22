from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')


class UserForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput,required=True)
	password = forms.CharField(widget=forms.PasswordInput,required=True)
	class Meta:
		model = User
		fields = ['username', 'password']

class RegisterForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput)
	email = forms.CharField(widget=forms.EmailInput)
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)
	nombre = forms.CharField(widget=forms.TextInput)
	apellido = forms.CharField(widget=forms.TextInput)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2','nombre','apellido']












    