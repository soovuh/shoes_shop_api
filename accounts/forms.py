from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'password')

    password = forms.CharField(widget=forms.PasswordInput(), label='Password')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')


class EmailForm(forms.Form):
    email = forms.EmailField()


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')
