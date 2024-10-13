from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['email', 'nome', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail')