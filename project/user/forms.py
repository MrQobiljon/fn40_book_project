from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'style': 'padding: 10px;'
            })
        }


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')